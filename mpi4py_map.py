#!/bin/env python

import sys
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
BARRIER = 123
EXIT = 2
WORK = 10


def mpi_map(function, sequence, *args, **kwargs):
    """Return a list of the results of applying the function in
    parallel (using mpi4py) to each element in sequence.
    :Arguments:
        function : python function
            Function to be called that takes as first argument an element of sequence.
        sequence : list
            Sequence of elements supplied to function.
    :Optional:
        args : tuple
            Additional constant arguments supplied to function.
        debug : bool=False
              Be very verbose (for debugging purposes).
    """
    rank = comm.Get_rank()

    if rank == 0:
        # Controller
        result = _mpi_controller(sequence, *args, **kwargs)
        return result
    else:
        # Worker
        _mpi_worker(function, sequence, *args, **kwargs)


def _mpi_controller(sequence, *args, **kwargs):
    """Controller function that sends each element in sequence to
    different workers. Handles queueing and job termination.
    :Arguments:
        sequence : list
            Sequence of elements supplied to the workers.
    :Optional:
        args : tuple
            Additional constant arguments supplied to function.
        debug : bool=False
            Be very verbose (for debugging purposes).
    """
    debug = 'debug' in kwargs
    if debug:
        del kwargs['debug']

    rank = comm.Get_rank()
    assert rank == 0, "rank has to be 0."
    proc_name = MPI.Get_processor_name()
    status = MPI.Status()

    process_list = range(1, comm.Get_size())
    number_of_workers = len(process_list) * 1.0
    number_of_tasks = len(sequence) * 1.0
    print "Number of tasks:", number_of_tasks
    print "Number of workers:", number_of_workers
    last_percentage_tasks = 0.0
    last_percentage_workers = 0.0
    workers_done = []
    results = {}
    if debug: print "Data:", sequence

    # Instead of distributing the actual elements, we just distribute
    # the index as the workers already have the sequence. This allows
    # objects to be used as well.
    queue = iter(xrange(len(sequence)))

    print "Controller %i on %s: ready!" % (rank, proc_name)

    # Feed all queued jobs to the childs
    while(True):
        status = MPI.Status()
        # Receive input from workers.
        recv = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        if debug: print "Controller: received tag %i from %s" % (status.tag, status.source)

        if status.tag == 1 or status.tag == WORK or status.tag == BARRIER:
            # tag 1 codes for initialization.
            # tag WORK codes for requesting more data.
            if status.tag == WORK: # data received
                if debug: print "Controller: Job %i completed by %i" % (recv[0], status.source)
                results[recv[0]] = recv[1] # save back

            # Get next item and send to worker
            try:
                task = queue.next()
                percentage = task / number_of_tasks * 100
                if (percentage > last_percentage_tasks + 5.0):
                  print "Tasks done:", task, "/", int(number_of_tasks), "(", percentage, "%)"
                  last_percentage_tasks = percentage
                if sequence[task] == BARRIER:
                  if debug: print "Issueing barrier"
                  # comm.barrier()
                  for i in range(1, len(process_list) + 1):
                    if debug: print ('sending to i =    ', i)
                    comm.send([], dest=i, tag=BARRIER)
                  if debug: print "Continue after barrier"
                else:
                  # Send job to worker
                  if debug: print "Controller: Sending task to %i" % status.source
                  comm.send(task, dest=status.source, tag=WORK)

            except StopIteration:
                # Send kill signal
                if debug: print "Controller: Task queue is empty"
                workers_done.append(status.source)
                comm.send([], dest=status.source, tag=EXIT)

                # Task queue is empty
                if len(process_list) == 0:
                    break

        elif status.tag == EXIT:
            if recv != []:
                # Worker seems to have crashed but was nice enough to
                # send us the item number he has been working on
                results[recv[0]] = recv[1] # save back

            # print 'Process %i exited, removing.' % status.source
            process_list.remove(status.source)
            # print 'Processes left over: ' + str(process_list)
            percentage = (1 - len(process_list) / number_of_workers) * 100
            if (percentage > last_percentage_workers + 5.0):
              print "Inactive workers:", int(number_of_workers -
                  len(process_list)), "/", int(number_of_workers), "(", percentage, "%)"
              last_percentage_workers = percentage
            # Worker queue is empty
            if len(process_list) == 0:
                break

        else:
            print 'Unkown tag %i with msg %s' % (status.tag, str(recv))

    if len(process_list) == 0:
        if debug: print "All workers done."
        sorted_results = [results[i] for i in range(len(sequence)) if sequence[i] != BARRIER]
        if debug: print sorted_results
        return sorted_results
    else:
        raise IOError("Something went wrong, workers still active")
        print process_list
        return False

def _mpi_worker(function, sequence, *args, **kwargs):
    """Worker that applies function to each element it receives from
    the controller.
    :Arguments:
        function : python function
            Function to be called that takes as first argument an
            element received from the controller.
    :Optional:
        args : tuple
            Additional constant arguments supplied to function.
        debug : bool=False
            Be very verbose (for debugging purposes).
    """
    debug = 'debug' in kwargs
    if debug:
        del kwargs['debug']

    rank = comm.Get_rank()
    assert rank != 0, "rank is 0 which is reserved for the controller."
    proc_name = MPI.Get_processor_name()
    status = MPI.Status()
    time.sleep(1)
    print "Worker %i on %s: ready!" % (rank, proc_name)

    # Send ready signal
    comm.send([{'rank': rank, 'name':proc_name}], dest=0, tag=1)

    # Start main data loop
    while True:
        # Wait for element
        if debug: print "Worker %i on %s: waiting for data" % (rank, proc_name)
        recv = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        if debug: print "Worker %i on %s: received data, tag: %i" % (rank, proc_name, status.tag)
        if status.tag == EXIT:
            if debug: print "Worker %i on %s: received kill signal" % (rank, proc_name)
            comm.send([], dest=0, tag=EXIT)
            sys.exit(0)

        if status.tag == BARRIER:
            if debug: print "Worker %i on %s: received barrier signal" % (rank, proc_name)
            comm.send([], dest=0, tag=BARRIER)

        if status.tag == WORK:
            # Call function on received element
            if debug: print "Worker %i on %s: Calling function %s with %s" % (rank, proc_name, function.__name__, recv)

            try:
                result = function(sequence[recv], *args, **kwargs)
            except Exception as e:
                # Send to master that we are quitting
                print(e)
                comm.send((recv, None), dest=0, tag=EXIT)
                sys.exit(0)

            if debug: print("Worker %i on %s: finished job %i" % (rank, proc_name, recv))
            # Return sequence number and result to controller
            comm.send((recv, result), dest=0, tag=WORK)

