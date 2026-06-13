
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

### 1.5.2 Verification

```bash
cd ~/HPC-exercise/exercise1

# 1. Check that the binaries were actually created
ls -l bin/

# 2. Quick functional test (small run on the login node is fine for verification)
mpirun -np 4 ./bin/osu_bcast
```


### 1.6 OSU build

```bash
cd ~/HPC-exercise/exercise1/scripts

# Fix the permission
chmod +x make.sh

# Re-run with full logging
./make.sh 2>&1 | tee ~/osu_build.log

# Show us what happened
cat ~/osu_build.log
```

### 1.6.1 Quick Check

```bash
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ ls -l ../bin/
total 654
```

```
-rwxr-xr-x 1 ocusmafait ocusmafait 332720 Jun 11 12:33 osu_barrier
-rwxr-xr-x 1 ocusmafait ocusmafait 336696 Jun 11 12:33 osu_bcast
```

Excellent! This is the first time we've seen a clean, successful build. The two binaries are present, have reasonable size, and are executable. 

### 1.6.2 Verification

Before we touch the SLURM scripts, we should confirm that the compiled tools actually run.
Quick sanity test with `osu_bcast` (very small run):

```bash
module load openMPI/4.1.6

cd ~/HPC-exercise/exercise1

mpirun -np 4 ./bin/osu_bcast
```

```
# OSU MPI Broadcast Latency Test v7.3
# Datatype: MPI_CHAR.
# Size       Avg Latency(us)
1                       0.46
2                       0.48
4                       0.49
8                       0.48
16                      0.48
32                      0.63
64                      0.60
128                     1.16
256                     1.13
512                     1.13
1024                    1.50
2048                    2.10
4096                   15.08
8192                    4.84
16384                  13.38
32768                  18.13
65536                  27.00
131072                 39.86
262144                 69.12
524288                142.41
1048576               627.75
```

Also test barrier quickly:
```bash
mpirun -np 4 ./bin/osu_barrier
```

```
# OSU MPI Barrier Latency Test v7.3
# Avg Latency(us)
             1.41
```

• The two binaries (`osu_bcast` and `osu_barrier`) were successfully compiled with openMPI/4.1.6.
• They are executable and produce normal OSU output (the small 4-process test ran without crashing and gave reasonable latencies for a quick check).


> *Generate a GitHub token for Orfeo to push any changes in the repo.*

---

### 2.0 Sbatch the jobs 

Now we submit the four jobs. Run these commands on Orfeo:

```bash
cd ~/HPC-exercise/exercise1/scripts

sbatch bcast_latencies.sh      # EPYC bcast
sbatch barrier_latencies.sh    # EPYC barrier
sbatch bcast_thin.sh           # THIN bcast
sbatch barrier_thin.sh         # THIN barrier
```

```
Submitted batch job 1277489
Submitted batch job 1277494
Submitted batch job 1277502
Submitted batch job 1277506
```


### 2.0.1 Check

Then immediately check the queue:

```bash
squeue -u $USER
```

```bash
JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
1277489      EPYC ex1EPYCb ocusmafa PD       0:00      2 (Resources)
1277494      EPYC ex1EPYCa ocusmafa PD       0:00      2 (Priority)
1277506      THIN ex1THINa ocusmafa PD       0:00      2 (Priority)
1277502      THIN ex1THINb ocusmafa PD       0:00      2 (Priority)
```

If you ever want to see only the real jobs, you can do:
```bash
sacct -u $USER --format=JobID,JobName,Partition,State,ExitCode,Elapsed --starttime=today | grep -v '\.'
```

```bash
ocusmafait@login02:~$ sacct -u $USER --format=JobID,JobName,Partition,State,ExitCode,Elapsed --starttime=today | grep -v '\.'
JobID           JobName  Partition      State ExitCode    Elapsed
------------ ---------- ---------- ---------- -------- ----------
1277502       ex1THINbc       THIN    PENDING      0:0   00:00:00
1277506      ex1THINarr       THIN    PENDING      0:0   00:00:00
```



---
