#! /usr/bin/env python3

"""
AdjHE command line argument parser
Christian Coffman: coffm049@umn.edu
Created 2022-05-26
Last Updated 2022-06-06
"""

##############################################################
# This is a helper tool for the AdjHE estimator that takes 
# command line arguments and converts them for use in AdjHE 
# heritability estimation
##############################################################

import argparse
import json 
from Estimate.data_input.parser import readable_file_or_none, readable_json

#%%

def get_args() :
    """
    Collects user input from command line and returns them for running with Estimate.

    Returns
    -------
    dictionary of user arguments from command line

    """
    # Create arg parser
    parser = argparse.ArgumentParser(
        prog='Running adjusted HE regression',description="This program gives estimation in formula fashion." 
        "Make sure you have enough memory to store GRM matrix in python.")
    
        
    # Or accept a file with all arguments
    parser.add_argument("--argfile", 
                        # type=readable_json,
                        metavar= "ARGFILE_FILE_PATH", 
                        help="Filename to be passed containing all information for simulations", 
                        default=None)    
    parser.add_argument("--out", 
                        metavar= "OUT_FILE_PATH", 
                        help="Filename to be save results.", 
                        default=None)    

    
    # return the arguments as a dictionary
    args = vars(parser.parse_args())
    with open(args['argfile']) as f:
        args2 = json.load(f)
        
    args2["out"] = args["out"]

    return args2
