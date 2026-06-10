
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
Lmod has detected the following error:  The
following module(s) are unknown:
"openMPI/4.1.5/gnu/12.2.1"

Please check the spelling or version number. Also try
"module spider ..."
It is also possible your cache file is out-of-date; it
may help to try:
  $ module --ignore_cache load "openMPI/4.1.5/gnu/12.2.1"

Also make sure that all modulefiles written in TCL start
with the string #%Module



Saving 'osu-micro-benchmarks-7.3.tar.gz'
HTTP response 200 OK [https://mvapich.cse.ohio-state.edu/dosu-micro-benchmarks 100% [=======>]  924.98K    3.03MB/s
                          [Files: 1]
osu-micro-benchmarks-7.3/
osu-micro-benchmarks-7.3/.clang-format
osu-micro-benchmarks-7.3/CHANGES
osu-micro-benchmarks-7.3/COPYRIGHT
osu-micro-benchmarks-7.3/Makefile.am
osu-micro-benchmarks-7.3/README
osu-micro-benchmarks-7.3/c/
osu-micro-benchmarks-7.3/c/Makefile.am
osu-micro-benchmarks-7.3/c/get_local_rank
osu-micro-benchmarks-7.3/c/mpi/
osu-micro-benchmarks-7.3/c/mpi/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/collective/
osu-micro-benchmarks-7.3/c/mpi/collective/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_allgather.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_allgatherv.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_allreduce.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_alltoall.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_alltoallv.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_alltoallw.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_barrier.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_bcast.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_gather.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_gatherv.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_reduce.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_reduce_scatter.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_scatter.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_scatterv.c
osu-micro-benchmarks-7.3/c/mpi/collective/blocking/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_ineighbor_allgather.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_ineighbor_allgatherv.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_ineighbor_alltoall.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_ineighbor_alltoallv.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_ineighbor_alltoallw.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_neighbor_allgather.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_neighbor_allgatherv.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_neighbor_alltoall.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_neighbor_alltoallv.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/osu_neighbor_alltoallw.c
osu-micro-benchmarks-7.3/c/mpi/collective/neighborhood/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_iallgather.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_iallgatherv.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_iallreduce.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_ialltoall.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_ialltoallv.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_ialltoallw.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_ibarrier.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_ibcast.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_igather.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_igatherv.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_ireduce.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_ireduce_scatter.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_iscatter.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/osu_iscatterv.c
osu-micro-benchmarks-7.3/c/mpi/collective/non_blocking/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_allgather_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_allgatherv_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_allreduce_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_alltoall_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_alltoallv_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_alltoallw_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_barrier_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_bcast_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_gather_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_gatherv_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_reduce_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_reduce_scatter_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_scatter_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/osu_scatterv_persistent.c
osu-micro-benchmarks-7.3/c/mpi/collective/persistent/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/collective/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/one-sided/
osu-micro-benchmarks-7.3/c/mpi/one-sided/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_acc_latency.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_cas_latency.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_fop_latency.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_get_acc_latency.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_get_bw.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_get_latency.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_put_bibw.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_put_bw.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/osu_put_latency.c
osu-micro-benchmarks-7.3/c/mpi/one-sided/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/pt2pt/
osu-micro-benchmarks-7.3/c/mpi/pt2pt/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/pt2pt/persistent/
osu-micro-benchmarks-7.3/c/mpi/pt2pt/persistent/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/pt2pt/persistent/osu_bibw_persistent.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/persistent/osu_bw_persistent.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/persistent/osu_latency_persistent.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/persistent/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/osu_bibw.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/osu_bw.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/osu_latency.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/osu_latency_mp.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/osu_latency_mt.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/osu_mbw_mr.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/osu_multi_lat.c
osu-micro-benchmarks-7.3/c/mpi/pt2pt/standard/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/pt2pt/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/startup/
osu-micro-benchmarks-7.3/c/mpi/startup/Makefile.am
osu-micro-benchmarks-7.3/c/mpi/startup/osu_hello.c
osu-micro-benchmarks-7.3/c/mpi/startup/osu_init.c
osu-micro-benchmarks-7.3/c/mpi/startup/Makefile.in
osu-micro-benchmarks-7.3/c/mpi/Makefile.in
osu-micro-benchmarks-7.3/c/openshmem/
osu-micro-benchmarks-7.3/c/openshmem/Makefile.am
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_atomics.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_barrier.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_broadcast.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_collect.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_fcollect.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_get.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_get_mr_nb.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_get_nb.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_put.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_put_mr.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_put_mr_nb.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_put_nb.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_put_overlap.c
osu-micro-benchmarks-7.3/c/openshmem/osu_oshm_reduce.c
osu-micro-benchmarks-7.3/c/openshmem/Makefile.in
osu-micro-benchmarks-7.3/c/upc/
osu-micro-benchmarks-7.3/c/upc/Makefile.am
osu-micro-benchmarks-7.3/c/upc/osu_upc_all_barrier.c
osu-micro-benchmarks-7.3/c/upc/osu_upc_all_broadcast.c
osu-micro-benchmarks-7.3/c/upc/osu_upc_all_exchange.c
osu-micro-benchmarks-7.3/c/upc/osu_upc_all_gather.c
osu-micro-benchmarks-7.3/c/upc/osu_upc_all_gather_all.c
osu-micro-benchmarks-7.3/c/upc/osu_upc_all_reduce.c
osu-micro-benchmarks-7.3/c/upc/osu_upc_all_scatter.c
osu-micro-benchmarks-7.3/c/upc/osu_upc_memget.c
osu-micro-benchmarks-7.3/c/upc/osu_upc_memput.c
osu-micro-benchmarks-7.3/c/upc/Makefile.in
osu-micro-benchmarks-7.3/c/upcxx/
osu-micro-benchmarks-7.3/c/upcxx/Makefile.am
osu-micro-benchmarks-7.3/c/upcxx/osu_upcxx_allgather.cpp
osu-micro-benchmarks-7.3/c/upcxx/osu_upcxx_alltoall.cpp
osu-micro-benchmarks-7.3/c/upcxx/osu_upcxx_async_copy_get.cpp
osu-micro-benchmarks-7.3/c/upcxx/osu_upcxx_async_copy_put.cpp
osu-micro-benchmarks-7.3/c/upcxx/osu_upcxx_bcast.cpp
osu-micro-benchmarks-7.3/c/upcxx/osu_upcxx_gather.cpp
osu-micro-benchmarks-7.3/c/upcxx/osu_upcxx_reduce.cpp
osu-micro-benchmarks-7.3/c/upcxx/osu_upcxx_scatter.cpp
osu-micro-benchmarks-7.3/c/upcxx/Makefile.in
osu-micro-benchmarks-7.3/c/util/
osu-micro-benchmarks-7.3/c/util/ddt_sample.txt
osu-micro-benchmarks-7.3/c/util/kernel.cu
osu-micro-benchmarks-7.3/c/util/nhbrhd_graph.adj
osu-micro-benchmarks-7.3/c/util/osu_util.c
osu-micro-benchmarks-7.3/c/util/osu_util.h
osu-micro-benchmarks-7.3/c/util/osu_util_graph.c
osu-micro-benchmarks-7.3/c/util/osu_util_graph.h
osu-micro-benchmarks-7.3/c/util/osu_util_mpi.c
osu-micro-benchmarks-7.3/c/util/osu_util_mpi.h
osu-micro-benchmarks-7.3/c/util/osu_util_options.h
osu-micro-benchmarks-7.3/c/util/osu_util_papi.c
osu-micro-benchmarks-7.3/c/util/osu_util_papi.h
osu-micro-benchmarks-7.3/c/util/osu_util_pgas.c
osu-micro-benchmarks-7.3/c/util/osu_util_pgas.h
osu-micro-benchmarks-7.3/c/util/osu_util_validation.c
osu-micro-benchmarks-7.3/c/xccl/
osu-micro-benchmarks-7.3/c/xccl/Makefile.am
osu-micro-benchmarks-7.3/c/xccl/collective/
osu-micro-benchmarks-7.3/c/xccl/collective/Makefile.am
osu-micro-benchmarks-7.3/c/xccl/collective/osu_xccl_allgather.c
osu-micro-benchmarks-7.3/c/xccl/collective/osu_xccl_allreduce.c
osu-micro-benchmarks-7.3/c/xccl/collective/osu_xccl_alltoall.c
osu-micro-benchmarks-7.3/c/xccl/collective/osu_xccl_bcast.c
osu-micro-benchmarks-7.3/c/xccl/collective/osu_xccl_reduce.c
osu-micro-benchmarks-7.3/c/xccl/collective/osu_xccl_reduce_scatter.c
osu-micro-benchmarks-7.3/c/xccl/collective/Makefile.in
osu-micro-benchmarks-7.3/c/xccl/pt2pt/
osu-micro-benchmarks-7.3/c/xccl/pt2pt/Makefile.am
osu-micro-benchmarks-7.3/c/xccl/pt2pt/osu_xccl_bibw.c
osu-micro-benchmarks-7.3/c/xccl/pt2pt/osu_xccl_bw.c
osu-micro-benchmarks-7.3/c/xccl/pt2pt/osu_xccl_latency.c
osu-micro-benchmarks-7.3/c/xccl/pt2pt/Makefile.in
osu-micro-benchmarks-7.3/c/xccl/util/
osu-micro-benchmarks-7.3/c/xccl/util/nccl/
osu-micro-benchmarks-7.3/c/xccl/util/nccl/osu_util_nccl_impl.c
osu-micro-benchmarks-7.3/c/xccl/util/nccl/osu_util_nccl_impl.h
osu-micro-benchmarks-7.3/c/xccl/util/osu_util_xccl_interface.c
osu-micro-benchmarks-7.3/c/xccl/util/osu_util_xccl_interface.h
osu-micro-benchmarks-7.3/c/xccl/util/rccl/
osu-micro-benchmarks-7.3/c/xccl/util/rccl/osu_util_rccl_impl.c
osu-micro-benchmarks-7.3/c/xccl/util/rccl/osu_util_rccl_impl.h
osu-micro-benchmarks-7.3/c/xccl/Makefile.in
osu-micro-benchmarks-7.3/c/Makefile.in
osu-micro-benchmarks-7.3/configure.ac
osu-micro-benchmarks-7.3/java/
osu-micro-benchmarks-7.3/java/README
osu-micro-benchmarks-7.3/java/mpi/
osu-micro-benchmarks-7.3/java/mpi/collective/
osu-micro-benchmarks-7.3/java/mpi/collective/OSUAllReduce.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUAllgather.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUAllgatherv.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUAlltoall.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUAlltoallv.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUBarrier.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUBcast.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUGather.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUGatherv.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUReduce.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUReduceScatter.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUScatter.java
osu-micro-benchmarks-7.3/java/mpi/collective/OSUScatterv.java
osu-micro-benchmarks-7.3/java/mpi/common/
osu-micro-benchmarks-7.3/java/mpi/common/BenchmarkUtils.java
osu-micro-benchmarks-7.3/java/mpi/pt2pt/
osu-micro-benchmarks-7.3/java/mpi/pt2pt/OSUBandwidth.java
osu-micro-benchmarks-7.3/java/mpi/pt2pt/OSUBandwidthOMPI.java
osu-micro-benchmarks-7.3/java/mpi/pt2pt/OSUBiBandwidth.java
osu-micro-benchmarks-7.3/java/mpi/pt2pt/OSUBiBandwidthOMPI.java
osu-micro-benchmarks-7.3/java/mpi/pt2pt/OSULatency.java
osu-micro-benchmarks-7.3/java/mpi/startup/
osu-micro-benchmarks-7.3/java/mpi/startup/HelloWorld.java
osu-micro-benchmarks-7.3/java/mpi/startup/OMPIHelloWorld.java
osu-micro-benchmarks-7.3/maint/
osu-micro-benchmarks-7.3/maint/omb-format.pl
osu-micro-benchmarks-7.3/map_rank_to_gpu
osu-micro-benchmarks-7.3/python/
osu-micro-benchmarks-7.3/python/.gitignore
osu-micro-benchmarks-7.3/python/Makefile.am
osu-micro-benchmarks-7.3/python/README
osu-micro-benchmarks-7.3/python/__init__.py
osu-micro-benchmarks-7.3/python/mpi/
osu-micro-benchmarks-7.3/python/mpi/__init__.py
osu-micro-benchmarks-7.3/python/mpi/collective/
osu-micro-benchmarks-7.3/python/mpi/collective/Makefile.am
osu-micro-benchmarks-7.3/python/mpi/collective/__init__.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_allgather.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_allgatherv.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_allreduce.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_alltoall.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_alltoallv.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_barrier.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_bcast.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_gather.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_gatherv.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_reduce.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_reduce_scatter.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_scatter.py
osu-micro-benchmarks-7.3/python/mpi/collective/osu_scatterv.py
osu-micro-benchmarks-7.3/python/mpi/pt2pt/
osu-micro-benchmarks-7.3/python/mpi/pt2pt/Makefile.am
osu-micro-benchmarks-7.3/python/mpi/pt2pt/__init__.py
osu-micro-benchmarks-7.3/python/mpi/pt2pt/osu_bibw.py
osu-micro-benchmarks-7.3/python/mpi/pt2pt/osu_bw.py
osu-micro-benchmarks-7.3/python/mpi/pt2pt/osu_latency.py
osu-micro-benchmarks-7.3/python/mpi/pt2pt/osu_multi_lat.py
osu-micro-benchmarks-7.3/python/run.py
osu-micro-benchmarks-7.3/python/util/
osu-micro-benchmarks-7.3/python/util/Makefile.am
osu-micro-benchmarks-7.3/python/util/__init__.py
osu-micro-benchmarks-7.3/python/util/options.py
osu-micro-benchmarks-7.3/python/util/osu_util_mpi.py
osu-micro-benchmarks-7.3/python/util/parser.py
osu-micro-benchmarks-7.3/autom4te.cache/
osu-micro-benchmarks-7.3/autom4te.cache/requests
osu-micro-benchmarks-7.3/autom4te.cache/traces.0
osu-micro-benchmarks-7.3/autom4te.cache/output.0
osu-micro-benchmarks-7.3/autom4te.cache/traces.1
osu-micro-benchmarks-7.3/autom4te.cache/output.1
osu-micro-benchmarks-7.3/ltmain.sh
osu-micro-benchmarks-7.3/aclocal.m4
osu-micro-benchmarks-7.3/configure
osu-micro-benchmarks-7.3/compile
osu-micro-benchmarks-7.3/config.guess
osu-micro-benchmarks-7.3/config.sub
osu-micro-benchmarks-7.3/install-sh
osu-micro-benchmarks-7.3/missing
osu-micro-benchmarks-7.3/Makefile.in
osu-micro-benchmarks-7.3/depcomp
checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for a thread-safe mkdir -p... /usr/bin/mkdir -p
checking for gawk... gawk
checking whether make sets $(MAKE)... yes
checking whether make supports nested variables... yes
checking build system type... x86_64-pc-linux-gnu
checking host system type... x86_64-pc-linux-gnu
checking how to print strings... printf
checking whether make supports the include directive... yes (GNU style)
checking for gcc... /usr/bin/mpicc
checking whether the C compiler works... no
configure: error: in `/u/dssc/ocusmafait/HPC-exercise/exercise1/osu-micro-benchmarks-7.3':
configure: error: C compiler cannot create executables
See `config.log' for more details
make: *** No targets specified and no makefile found.  Stop.
make: *** No rule to make target 'install'.  Stop.
mkdir: cannot create directory ‘bin’: File exists
cp: cannot stat 'osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_bcast': No such file or directory
cp: cannot stat 'osu-micro-benchmarks-7.3/c/mpi/collective/blocking/osu_barrier': No such file or directory
```

---

