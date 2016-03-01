if mpirun --version 2>&1 | grep Open; then
  time mpirun -np 4 ../mpi_generate.py `pwd`
else
  time mpirun -f ../host_file ../mpi_generate.py `pwd`
fi
