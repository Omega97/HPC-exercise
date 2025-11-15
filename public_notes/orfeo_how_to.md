
## Connect to Orfeo

1) Fire up Command Prompt as Admin `Win + X -> A`

2) Run WSL
```
wsl
```

3) Connect to Orfeo
```
ssh -i ~/.ssh/orfeo_key ocusmafait@195.14.102.215
```

Vai nella cartella del progetto, crea la cartella dell'esercizio, e git-clona il repo
```
cd ~/HPC-exercise/HPC-exercise/exercise1
mkdir -p ~/HPC-exercise && cd ~/HPC-exercise
git clone https://github.com/Omega97/HPC-exercise.git
cd ~/HPC-exercise/HPC-exercise/exercise1
```
