
# **Execution Log - Exercise 1**

> This is the detailed log of **Exercise 1** of the HPC project: *Comparison of different Open MPI algorithms for collective operations using the OSU Micro-Benchmarks on the Orfeo cluster*.

---

## 🔐 Accessing Orfeo

### 1.0 Open Command Prompt as Administrator
```
Win + X → A
```

### 1.1 Start WSL and connect to Orfeo
```bash
wsl
orfeo
```
(or manually: `ssh -i ~/.ssh/orfeo_key_new ocusmafait@195.14.102.215`)

### 1.2 Pull from Git
```bash
cd ~/HPC-exercise
git pull
cd exercise1
```

### 1.3  Create the required directories
```bash
mkdir -p bin results logs
```

### 1.4 Check your account and available partitions (important)
```bash
sacctmgr list associations Users=$(whoami) format=Account,User,Partition
```

```
   Account       User  Partition
---------- ---------- ----------
      dssc ocusmafait       epyc
      dssc ocusmafait        fat
      dssc ocusmafait        gpu
      dssc ocusmafait       thin
```

### 1.5 Compile the OSU benchmarks

The file `make.sh`: 
- loads a specific OpenMPI version. This is important because OSU must be compiled against the MPI you will use later. 
- It downloads the OSU Micro-Benchmarks, and 
- configures the build.

```bash
cd scripts
chmod +x make.sh
./make.sh
```

```bash
Saving 'osu-micro-benchmarks-7.3.tar.gz'
HTTP response 200 OK [https://mvapich.cse.ohio-state.edu/dosu-micro-benchmarks 100% [=======>]  924.98K    --.-KB/s
                          [Files: 1]
osu-micro-benchmarks-7.3/
osu-micro-benchmarks-7.3/.clang-format
osu-micro-benchmarks-7.3/CHANGES
osu-micro-benchmarks-7.3/COPYRIGHT
osu-micro-benchmarks-7.3/Makefile.am

...

config.status: creating c/mpi/collective/non_blocking/Makefile
config.status: creating c/mpi/collective/neighborhood/Makefile
config.status: creating c/mpi/collective/persistent/Makefile
config.status: executing depfiles commands
config.status: executing libtool commands
Making all in c
make[1]: Entering directory '/orfeo/cephfs/home/dssc/ocusmafait/HPC-exercise/exercise1/osu-micro-benchmarks-7.3/c'
make[2]: Entering directory '/orfeo/cephfs/home/dssc/ocusmafait/HPC-exercise/exercise1/osu-micro-benchmarks-7.3/c'
make[2]: Nothing to be done for 'all-am'.
make[2]: Leaving directory '/orfeo/cephfs/home/dssc/ocusmafait/HPC-exercise/exercise1/osu-micro-benchmarks-7.3/c'
make[1]: Leaving directory '/orfeo/cephfs/home/dssc/ocusmafait/HPC-exercise/exercise1/osu-micro-benchmarks-7.3/c'
make[1]: Entering directory '/orfeo/cephfs/home/dssc/ocusmafait/HPC-exercise/exercise1/osu-micro-benchmarks-7.3'
make[1]: Nothing to be done for 'all-am'.
make[1]: Leaving directory '/orfeo/cephfs/home/dssc/ocusmafait/HPC-exercise/exercise1/osu-micro-benchmarks-7.3'
cp: cannot stat 'osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_bcast': No such file or directory
cp: cannot stat 'osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_barrier': No such file or directory
OSU benchmarks compiled successfully with openMPI/4.1.6
total 0
```

#### 1.5.2 Verification

```bash
cd ~/HPC-exercise/exercise1

# 1. Check that the binaries were actually created
ls -l bin/

# 2. Quick functional test (small run on the login node is fine for verification)
mpirun -np 4 ./bin/osu_bcast
```

---

