module load openMPI/4.1.6

# Go to exercise1 directory
cd ..

# Download and build OSU Micro-Benchmarks
wget https://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.3.tar.gz
tar -xvf osu-micro-benchmarks-7.3.tar.gz
rm -f osu-micro-benchmarks-7.3.tar.gz

cd osu-micro-benchmarks-7.3
./configure CC=mpicc
make -j

# Copy only the benchmarks we need
cd ..
mkdir -p bin
cp osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_bcast bin/
cp osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_barrier bin/

# Clean up
rm -rf osu-micro-benchmarks-7.3

if [ -f bin/osu_bcast ] && [ -f bin/osu_barrier ]; then
    echo "OSU benchmarks compiled successfully with openMPI/4.1.6"
    ls -l bin/
else
    echo "ERROR: Build failed - binaries not found in bin/"
    ls -l bin/
    exit 1
fi