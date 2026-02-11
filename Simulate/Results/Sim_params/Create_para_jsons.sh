#!/bin/bash -l        

module load python3

# Make json files for parallel simulations
# python ../../simulation_parallelizer.py --argfile Covariates_non_random_sites.json 
# run from project root
python Simulate/hpc_utilities/simulation_parallelizer.py --argfile Simulate/Results/Sim_params/Covariates_non_random_sites_0.25.json 


