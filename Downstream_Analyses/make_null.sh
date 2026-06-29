#!/bin/bash -l
#SBATCH --time=08:00:00
#SBATCH --ntasks=1
#SBATCH --mem=100g
#SBATCH --tmp=10g
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-user=sixxx054@umn.edu

cd /home/myersc/sixxx054/BridGE-Python/
source /common/software/install/migrated/anaconda/python3-2020.07-mamba/bin/activate
conda init bash
conda activate BridGE-env
source setup.sh

python3 make_null.py
