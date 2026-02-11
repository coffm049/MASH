#! /usr/bin/env python3

"""
AdjHE estimator
Christian Coffman: coffm049@umn.edu
Created 2022-05-26
Last Updated 2022-06-06
"""

##############################################################
# Simulation runner for AdjHE package 
##############################################################
import logging
from Estimate.data_input.sim_parser import get_args
import itertools
import json


#%% Get command line arguments
# Get CL arguments and convert them to usable Python objects in a dictionary
#args= read_flags({"argfile" : "Simulations/Sim_params/Adding_sites_clusts.json"})
args = get_args()
logging.info("Simulating with the following parameters:")
logging.info(args)


sigmas = []
for sg, ss, se in itertools.product(args["sgs"], args["sss"], args["ses"]) :
    if sg + ss + se == 1 :
        if sg != 0 :
            sigmas += [[sg, ss, se]]
        elif (sg ==0) and (ss == 0) :
            sigmas += [[sg, ss, se]]
#%%
def write_sim_json(nsubjectss = args["nsubjectss"], 
              sigmas = sigmas,
              site_comps = args["site_comps"],
              nsites = args["nsites"],
              theta_alleless = args["theta_alleless"],
              nclustss = args["nclustss"],
              dominances= args["dominances"],
              prop_causals= args["prop_causals"],
              site_deps=args["site_deps"] ,
              nnpcs = args["nnpcs"],
              nSNPss= args["nSNPss"],
              phenss= args["phenss"],
              reps = args["reps"], 
              site_het = args["site_het"],
              races_differ = False,
              cov_effect=True,
              ortho_cov = True,
              random_BS = args["random_BS"]) :
    """
    Takes an overarching simulation setup from json and splits it into individual simulations and furthermore splits them into 10 simulations 
    to make it run more in parallel

    Parameters
    ----------
    nsubjectss : TYPE, optional
        DESCRIPTION. The default is args["nsubjectss"].
    sigmas : TYPE, optional
        DESCRIPTION. The default is sigmas.
    site_comps : TYPE, optional
        DESCRIPTION. The default is args["site_comps"].
    nsites : TYPE, optional
        DESCRIPTION. The default is args["nsites"].
    theta_alleless : TYPE, optional
        DESCRIPTION. The default is args["theta_alleless"].
    nclustss : TYPE, optional
        DESCRIPTION. The default is args["nclustss"].
    dominances : TYPE, optional
        DESCRIPTION. The default is args["dominances"].
    prop_causals : TYPE, optional
        DESCRIPTION. The default is args["prop_causals"].
    site_deps : TYPE, optional
        DESCRIPTION. The default is args["site_deps"].
    nnpcs : TYPE, optional
        DESCRIPTION. The default is args["nnpcs"].
    nSNPss : TYPE, optional
        DESCRIPTION. The default is args["nSNPss"].
    phenss : TYPE, optional
        DESCRIPTION. The default is args["phenss"].
    reps : TYPE, optional
        DESCRIPTION. The default is args["reps"].
    site_het : TYPE, optional
        DESCRIPTION. The default is args["site_het"].

    Returns
    -------
    None.

    """
    for (nsubjects, sigma, site_comp, nsite,
         theta_alleles, nclusts, dominance, prop_causal,
         site_dep, nSNPs, phens,
         __) in itertools.product(nsubjectss, sigmas, site_comps, nsites,
                                theta_alleless, nclustss, dominances, prop_causals,
                                site_deps, nSNPss, phenss,
                                range(reps)) :
        # Write a separate json for each set of simulations in order to allow separate sbatches to be called in parallel
        data = {"nsubjectss": [nsubjects],
                "sgs" : [sigma[0]],
                "sss" : [sigma[1]],
                "ses" : [sigma[2]],
                "site_comps" : [site_comp],
                "nsites" : [nsite],
                "theta_alleless" : [theta_alleles],
                "nclustss" : [nclusts],
                "dominances" : [dominance],
                "prop_causals" : [prop_causal],
                "site_deps" : [site_dep],
                "nnpcs" :nnpcs,
                "nSNPss" : [nSNPs],
                "phenss" : [phens],
                "reps" : args["reps"],
                "all_ests" : True,
                "site_het" : False,
                "races_differ" : True,
                "cov_effect" : True,
                "ortho_cov" : True,
                "random_BS" : args["random_BS"]
                } 
        with open(f'Simulate/Results/Sim_params/Temp/{nsubjects}{sigma[0]}{sigma[1]}{sigma[2]}{site_comp}{nsite}{theta_alleles}{nclusts}{dominance}{prop_causal}{site_dep}{nSNPs}{phens}{races_differ}{cov_effect}{ortho_cov}{random_BS}{__}.json', 'w') as fp:
            json.dump(data, fp, indent = 4)

        
        
#%%

write_sim_json(nsubjectss = args["nsubjectss"], 
              sigmas = sigmas,
              site_comps = args["site_comps"],
              nsites = args["nsites"],
              theta_alleless = args["theta_alleless"],
              nclustss = args["nclustss"],
              dominances= args["dominances"],
              prop_causals= args["prop_causals"],
              site_deps=args["site_deps"] ,
              nnpcs = args["nnpcs"],
              nSNPss= args["nSNPss"],
              phenss= args["phenss"],
              reps = args["reps"], 
              site_het = args["site_het"],
              races_differ = True,
              cov_effect=True,
              ortho_cov = True,
              random_BS = args["random_BS"])
