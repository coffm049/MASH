#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 07:35:15 2022

@author: christian
"""
import os
import subprocess
import numpy as np
import pandas as pd 
from functions.Data_input.load_data import load_everything
# os.chdir("/home/christian/Research/Stat_gen/tools/Basu_herit")

#%%
def GCTA(df, covars, nnpc, mp, GRM, silent=False):
    # Store random integer to save to temp file name
    rng = np.random.default_rng()    
    numb = rng.integers(10000)
    temp_name = "temp" + str(numb)

    # write the phenotype file
    df[["FID", "IID", mp]].to_csv(temp_name + "_pheno.txt", sep = " ", header = False, index= False, na_rep = "NA")
    
    # Select the remaining variables of interest
    pcs =  ["pc_" + str(s) for s in range(1, nnpc)]
    df = df[["FID", "IID"] + covars + pcs]


    # Decide which are qcovars and which are discrete covars
    discrete = [(len(df[col].unique()) < 50) and (len(df[col].unique()) > 1) for col in df]
    # Include FID IID
    cont = [not v for v in discrete]
    discrete[0:2] = [True, True]

    
    # Svae temp files if there were any covariates in either category
    if sum(discrete) > 2:
        df.iloc[:,discrete].to_csv(temp_name + "_Discrete.txt", sep = " ", header = False, index= False, na_rep = "NA")
    if sum(cont) > 2:
        df.iloc[:,cont].to_csv(temp_name + "_Cont.txt", sep = " ", header= False, index= False, na_rep = "NA")
    
    #######################
    # Write GRM and ids
    # Specify information about binary GRM format
    dt = np.dtype('f4') # Relatedness is stored as a float of size 4 in the binary file
    
    
    # Write IDs
    df[["FID", "IID"]].to_csv(temp_name + ".grm.id", sep = " ", header= False, index= False)
    n = df.shape[0]
    
    l= np.tril_indices(n)
    
    # Write GRM to binary 
    GRM[l].astype("f4").tofile(temp_name + ".grm.bin")    
    ##############################
        
    # Format string for controlling variables
    covars = " "
    if os.path.exists(temp_name + "_Cont.txt") :
        covars += " --qcovar " + temp_name + "_Cont.txt "
    if os.path.exists(temp_name + "_Discrete.txt") : 
        covars += " --covar " + temp_name + "_Discrete.txt "
    
    # Find GCTA
    gcta = "whereis gcta64"
    gcta, __ = subprocess.Popen(
        gcta.split(), stdout=subprocess.PIPE).communicate()
    gcta= gcta.split()[1].decode("utf-8")

    
    # run gcta
    bashcommand = gcta + " --grm " + temp_name + " --pheno " + temp_name + "_pheno.txt --mpheno 1 --reml --out " + temp_name + " " + covars
    process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
    __output, __error = process.communicate()

    # parse output for estimate
    df = pd.read_table(temp_name + ".hsq", sep="\t").query( "Source == 'V(G)/Vp'").reset_index()
    
    result = {"h2" : df.Variance[0],
              "SE" : df.SE[0],
              "Pheno" : mp,
              "PCs" : nnpc,
              "Covariates" : "+".join(covars),
              "Time for analysis(s)" : 0,
              "Memory Usage" : 0}
    
    # tidy up by removing temporary files
    if os.path.exists(temp_name + "_Discrete.txt") : 
        os.remove(temp_name + "_Discrete.txt")
    if os.path.exists(temp_name + "_Discrete.txt") : 
        os.remove(temp_name + "_Cont.txt")
    if os.path.exists(temp_name + ".hsq") : 
        os.remove(temp_name + ".hsq")
    if os.path.exists(temp_name + ".log") : 
        os.remove(temp_name + ".log")


    
    # Return the fit results
    return pd.DataFrame(result, index = [0])

        



