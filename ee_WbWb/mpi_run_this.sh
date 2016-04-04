if mpirun --version 2>&1 | grep Open; then
  time mpirun -np 4 nice -n 11 ../mpi_generate.py `pwd`
elif mpirun --version | grep Intel; then
  time mpirun -n 4 nice -n 11 ../mpi_generate.py `pwd`
else
  time mpirun -f ../host_file nice -n 11 ../mpi_generate.py `pwd`
fi
