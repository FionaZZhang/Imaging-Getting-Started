#!/bin/bash
#SBATCH --job-name=my-job
#SBATCH --time=05:00:00
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH cpus-per-task=1
module load python/3.8.3
python ./uploads/control.py ./uploads/trial.py 1