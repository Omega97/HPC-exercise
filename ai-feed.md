
```bash
ocusmafait@login02:~$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
ocusmafait@login02:~$ sacct -u $USER --starttime=2026-06-11 --format=JobID,JobName,Partition,State,ExitCode,Elapsed | grep -v '\.'
JobID           JobName  Partition      State ExitCode    Elapsed
------------ ---------- ---------- ---------- -------- ----------
1277489       ex1EPYCbc       EPYC    TIMEOUT      0:0   02:00:07
1277494      ex1EPYCarr       EPYC    TIMEOUT      0:0   02:00:27
1277502       ex1THINbc       THIN  COMPLETED      0:0   00:11:33
1277506      ex1THINarr       THIN  COMPLETED      0:0   00:22:32
ocusmafait@login02:~$
```

```bash
ocusmafait@login02:~$ cd ~/HPC-exercise/exercise1
ocusmafait@login02:~/HPC-exercise/exercise1$ ls -lh results/bcastTHIN.csv results/barrierTHIN.csv
-rw-r--r-- 1 ocusmafait ocusmafait 6.4K Jun 15 20:48 results/barrierTHIN.csv
-rw-r--r-- 1 ocusmafait ocusmafait  88K Jun 15 10:24 results/bcastTHIN.csv
ocusmafait@login02:~/HPC-exercise/exercise1$ echo "bcastTHIN lines: $(wc -l < results/bcastTHIN.csv)"
bcastTHIN lines: 5881
ocusmafait@login02:~/HPC-exercise/exercise1$ echo "barrierTHIN lines: $(wc -l < results/barrierTHIN.csv)"
barrierTHIN lines: 561
ocusmafait@login02:~/HPC-exercise/exercise1$
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1$ cp results/barrierEPYC.csv results/barrierEPYC_partial.csv
ocusmafait@login02:~/HPC-exercise/exercise1$ rm results/barrierEPYC.csv
ocusmafait@login02:~/HPC-exercise/exercise1$ sed -i 's/#SBATCH --time=02:00:00/#SBATCH --time=04:00:00/' scripts/barrier_latencies.sh
ocusmafait@login02:~/HPC-exercise/exercise1$ cd scripts
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ sbatch barrier_latencies.sh
Submitted batch job 1303325
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ scancel 1303325
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ sed -i 's/#SBATCH --time=04:00:00/#SBATCH --time=02:00:00/' ~/HPC-exercise/exercise1/scripts/
sed: couldn't edit /u/dssc/ocusmafait/HPC-exercise/exercise1/scripts/: not a regular file
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ barrier_latencies.sh
-bash: barrier_latencies.sh: command not found
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$
```

---

```bash
ocusmafait@login02:~$ cd ~/HPC-exercise/exercise1/scripts
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ grep '#SBATCH --time' barrier_latencies.sh
#SBATCH --time=04:00:00
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ ls -lh ../results/barrierEPYC.csv ../results/barrierEPYC_partial.csv ../results/bcastEPYC.csv
ls: cannot access '../results/barrierEPYC.csv': No such file or directory
-rw-r--r-- 1 ocusmafait ocusmafait 4.1K Jun 19 16:48 ../results/barrierEPYC_partial.csv
-rw-r--r-- 1 ocusmafait ocusmafait 113K Jun 11 22:42 ../results/bcastEPYC.csv
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ cd ~/HPC-exercise/exercise1/scripts
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ sed -i 's/#SBATCH --time=04:00:00/#SBATCH --time=02:00:00/' barrier_latencies.sh
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ sed -i 's/iterations=20/iterations=10/' barrier_latencies.sh
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ sed -i 's/-i 1e4/-i 500/; s/-x 1e4/-x 500/' barrier_latencies.sh
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ grep -E '#SBATCH --time|iterations=|-i |-x ' barrier_latencies.sh
#SBATCH --time=02:00:00
iterations=10
          -i 500 \
          -x 500)
#   -i 500 \  # Set the number of warm-up iterations
#   -x 500) # Set the number of total iterations
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ sbatch barrier_latencies.sh
Submitted batch job 1303630
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           1303630      EPYC ex1EPYCa ocusmafa  R       1:53      2 epyc[001-002]
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ cd ~/HPC-exercise/exercise1
ocusmafait@login02:~/HPC-exercise/exercise1$ echo "bcastEPYC lines: $(wc -l < results/bcastEPYC.csv)"

for algo in 0 1 2 5; do
  echo -n "Algo $algo: "
  awk -F, -v a=$algo '$1==a {print $2}' results/bcastEPYC.csv | sort -n | uniq | tail -1
done
bcastEPYC lines: 7309
Algo 0: 256
Algo 1: 256
Algo 2: 256
Algo 5: 256
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1$ sacct -j 1303630 --format=JobID,State,ExitCode,Elapsed
JobID             State ExitCode    Elapsed
------------ ---------- -------- ----------
1303630         RUNNING      0:0   00:06:22
1303630.bat+    RUNNING      0:0   00:06:22
1303630.ext+    RUNNING      0:0   00:06:22
1303630.0     COMPLETED      0:0   00:00:10
1303630.1     COMPLETED      0:0   00:00:15
1303630.2     COMPLETED      0:0   00:00:21
1303630.3     COMPLETED      0:0   00:00:30
1303630.4     COMPLETED      0:0   00:00:42
1303630.5     COMPLETED      0:0   00:01:00
1303630.6     COMPLETED      0:0   00:01:21
1303630.7     COMPLETED      0:0   00:01:50
1303630.8     COMPLETED      0:0   00:02:28
1303630.9     COMPLETED      0:0   00:03:06
1303630.10    COMPLETED      0:0   00:03:44
1303630.11    COMPLETED      0:0   00:04:23
1303630.12    COMPLETED      0:0   00:04:28
1303630.13    COMPLETED      0:0   00:04:33
1303630.14    COMPLETED      0:0   00:04:40
1303630.15    COMPLETED      0:0   00:04:48
1303630.16    COMPLETED      0:0   00:05:01
1303630.17    COMPLETED      0:0   00:05:18
1303630.18    COMPLETED      0:0   00:05:39
1303630.19    COMPLETED      0:0   00:06:08
1303630.20      RUNNING      0:0   00:06:22
ocusmafait@login02:~/HPC-exercise/exercise1$ cd ~/HPC-exercise/exercise1
ocusmafait@login02:~/HPC-exercise/exercise1$ wc -l results/barrierEPYC.csv
21 results/barrierEPYC.csv
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1$ sacct -j 1303630 --format=JobID,State,ExitCode,Elapsed | head -5
JobID             State ExitCode    Elapsed
------------ ---------- -------- ----------
1303630         RUNNING      0:0   00:23:23
1303630.bat+    RUNNING      0:0   00:23:23
1303630.ext+    RUNNING      0:0   00:23:23
ocusmafait@login02:~/HPC-exercise/exercise1$ wc -l ~/HPC-exercise/exercise1/results/barrierEPYC.csv
69 /u/dssc/ocusmafait/HPC-exercise/exercise1/results/barrierEPYC.csv
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1$ sacct -j 1303630 --format=JobID,State,ExitCode,Elapsed | head -3
JobID             State ExitCode    Elapsed
------------ ---------- -------- ----------
1303630         RUNNING      0:0   00:26:48
ocusmafait@login02:~/HPC-exercise/exercise1$ wc -l ~/HPC-exercise/exercise1/results/barrierEPYC.csv
79 /u/dssc/ocusmafait/HPC-exercise/exercise1/results/barrierEPYC.csv
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           1303630      EPYC ex1EPYCa ocusmafa  R      36:17      2 epyc[001-002]
```

```bash
ocusmafait@login02:~/HPC-exercise/results$ wc -l ~/HPC-exercise/exercise1/results/barrierEPYC.csv
274 /u/dssc/ocusmafait/HPC-exercise/exercise1/results/barrierEPYC.csv
ocusmafait@login02:~/HPC-exercise/results$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           1303630      EPYC ex1EPYCa ocusmafa  R    1:38:04      2 epyc[001-002]
```

```bash
ocusmafait@login02:~$ sacct -j 1303630 --format=JobID,State,ExitCode,Elapsed | head -3
JobID             State ExitCode    Elapsed
------------ ---------- -------- ----------
1303630         TIMEOUT      0:0   02:00:00
ocusmafait@login02:~$ wc -l ~/HPC-exercise/exercise1/results/barrierEPYC.csv
335 /u/dssc/ocusmafait/HPC-exercise/exercise1/results/barrierEPYC.csv
```

```bash
ocusmafait@login02:~$ squeue -u $USER
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
ocusmafait@login02:~$ sacct -j 1303667 --format=JobID,State,ExitCode,Elapsed | head -3
JobID             State ExitCode    Elapsed
------------ ---------- -------- ----------
1303667         TIMEOUT      0:0   01:00:15
ocusmafait@login02:~$ wc -l ~/HPC-exercise/exercise1/results/barrierEPYC_alg01.csv
168 /u/dssc/ocusmafait/HPC-exercise/exercise1/results/barrierEPYC_alg01.csv
```

```bash
ocusmafait@login02:~$ cd ~/HPC-exercise
ocusmafait@login02:~/HPC-exercise$ git pull
remote: Enumerating objects: 11, done.
remote: Counting objects: 100% (11/11), done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 6 (delta 5), reused 6 (delta 5), pack-reused 0 (from 0)
Unpacking objects: 100% (6/6), 506 bytes | 50.00 KiB/s, done.
From https://github.com/Omega97/HPC-exercise
   5d026c6..11e137c  main       -> origin/main
Updating 5d026c6..11e137c
error: Your local changes to the following files would be overwritten by merge:
        exercise1/scripts/barrier_latencies_alg01.sh
        exercise1/scripts/barrier_latencies_alg24.sh
Please commit your changes or stash them before you merge.
Aborting
ocusmafait@login02:~/HPC-exercise$ git checkout -- exercise1/scripts/barrier_latencies_alg01.sh exercise1/scripts/barrier_latencies_alg24.sh
ocusmafait@login02:~/HPC-exercise$ git pull
Updating 5d026c6..11e137c
Fast-forward
 exercise1/scripts/barrier_latencies_alg01.sh | 2 +-
 exercise1/scripts/barrier_latencies_alg24.sh | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
ocusmafait@login02:~/HPC-exercise$ cd exercise1
ocusmafait@login02:~/HPC-exercise/exercise1$ mv results/barrierEPYC_alg01.csv results/barrierEPYC_alg01_run1.csv
ocusmafait@login02:~/HPC-exercise/exercise1$ cd scripts
ocusmafait@login02:~/HPC-exercise/exercise1/scripts$ sbatch barrier_latencies_alg01.sh
Submitted batch job 1303691
```

```bash
ocusmafait@login02:~$ sacct -j 1303691 --format=JobID,State,ExitCode,Elapsed | head -3
JobID             State ExitCode    Elapsed
------------ ---------- -------- ----------
1303691       COMPLETED      0:0   01:26:11
ocusmafait@login02:~$ wc -l ~/HPC-exercise/exercise1/results/barrierEPYC_alg01.csv
240 /u/dssc/ocusmafait/HPC-exercise/exercise1/results/barrierEPYC_alg01.csv
ocusmafait@login02:~$ for algo in 0 1; do
  echo -n "Algo $algo rows: "
  awk -F, -v a=$algo '$1==a' ~/HPC-exercise/exercise1/results/barrierEPYC_alg01.csv | wc -l
done
Algo 0 rows: 120
Algo 1 rows: 119
```

```bash
ocusmafait@login02:~$ sacct -u $USER --starttime=today --format=JobID,JobName,State,ExitCode,Elapsed | grep -E 'JOBID|EPYCa24'
1303806      ex1EPYCa24  COMPLETED      0:0   01:26:39
ocusmafait@login02:~$ wc -l ~/HPC-exercise/exercise1/results/barrierEPYC_alg24.csv
241 /u/dssc/ocusmafait/HPC-exercise/exercise1/results/barrierEPYC_alg24.csv
ocusmafait@login02:~$ for algo in 2 4; do
  echo -n "Algo $algo rows: "
  awk -F, -v a=$algo '$1==a' ~/HPC-exercise/exercise1/results/barrierEPYC_alg24.csv | wc -l
done
Algo 2 rows: 120
Algo 4 rows: 120
```

```bash
ocusmafait@login02:~$ cd ~/HPC-exercise/exercise1/results

head -1 barrierEPYC_alg01.csv > barrierEPYC.csv
tail -n +2 barrierEPYC_alg01.csv >> barrierEPYC.csv
tail -n +2 barrierEPYC_alg24.csv >> barrierEPYC.csv

wc -l barrierEPYC.csv
480 barrierEPYC.csv
```

```bash
ocusmafait@login02:~/HPC-exercise/exercise1/results$ cd ~/HPC-exercise/exercise1/results

for f in bcastEPYC.csv barrierEPYC.csv bcastTHIN.csv barrierTHIN.csv; do
  echo "=== $f: $(wc -l < $f) lines ==="
done

echo "=== barrierEPYC per algo ==="
for algo in 0 1 2 4; do
  echo -n "Algo $algo: "
  awk -F, -v a=$algo '$1==a' barrierEPYC.csv | wc -l
done
=== bcastEPYC.csv: 7309 lines ===
=== barrierEPYC.csv: 480 lines ===
=== bcastTHIN.csv: 5881 lines ===
=== barrierTHIN.csv: 561 lines ===
=== barrierEPYC per algo ===
Algo 0: 120
Algo 1: 119
Algo 2: 120
Algo 4: 120
```

*On Windows:*
```bash
omar@LAPTOP-5NQPSH46:/mnt/c/Users/monfalcone$ scp -i ~/.ssh/orfeo_key_new \
    ocusmafait@195.14.102.215:~/HPC-exercise/exercise1/results/bcastEPYC.csv \
    ocusmafait@195.14.102.215:~/HPC-exercise/exercise1/results/barrierEPYC.csv \
    ocusmafait@195.14.102.215:~/HPC-exercise/exercise1/results/bcastTHIN.csv \
    ocusmafait@195.14.102.215:~/HPC-exercise/exercise1/results/barrierTHIN.csv \
    /mnt/c/Users/monfalcone/PycharmProjects/HPC-exercise/exercise1/results/
bcastEPYC.csv                                                                                    100%  113KB 536.1KB/s   00:00
barrierEPYC.csv                                                                                  100% 5139    98.5KB/s   00:00
bcastTHIN.csv                                                                                    100%   88KB   5.3KB/s   00:16
barrierTHIN.csv                                                                                  100% 6495   118.9KB/s   00:00
```

