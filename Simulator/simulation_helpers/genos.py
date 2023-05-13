#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate phenotypes
Created on Thu Oct 13 09:25:44 2022

@author: christian
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from Simulator.simulation_helpers.admixing import sample_admixed_genotypes


def sim_genos(seed, ancestral_frequencies, cluster_frequencies, subject_ancestries,
              clusters_differ = False, prop_causal=0.1, admixing = False):
    """
    Simulate genotypes of the subjects given their cluster ID and the respective cluster allele frequencies

    Parameters
    ----------
    seed : seed or numpy random number generator Generator object
        random number generator.
    cluster_frequencies : numpy array
        (nsubjects x nclusts) array contianing allele frequencies for each cluster.
    subject_ancestries : pandas series
        vector containng which ancestry each subject will be sampled from.
    clusters_differ : bool, optional
        should clusters have different means or should all the variations in the phenotype take place in non-cluster informative regions.
        The default is False.
    prop_causal : float, optional
        between 0 and 1 specifyin the number of SNPs that are causal. The default is 0.1.


    Returns
    -------
    tuple
    genotypes : numpy array
        (nsubjects x nSNPs array) containing subject genotypes.
    GRM : numpy array
        (nsubjects x nsubjects) array containing standardized genetic relatedness matrix .
    pcs : pandas dataframe
        dataframe containing loadings along all eigenvectors.

    """
    
    rng = np.random.default_rng(seed)
    nclusts = np.unique(subject_ancestries).shape[0]
    nsubjects = subject_ancestries.shape[0]
    
    if nclusts == 1:
        nSNPs = cluster_frequencies.shape[0]
        # simulate genotypes
        genotypes = rng.binomial(n=np.repeat(2, nSNPs), p=cluster_frequencies[0],
                                 size=(nsubjects, nSNPs))
    elif (nclusts > 1) and (not admixing)  :
        nSNPs = cluster_frequencies.shape[1]
        # simulate genotypes
        genotypes = rng.binomial(n=np.repeat(2, nSNPs), p= cluster_frequencies[subject_ancestries],
                                 size=(nsubjects, nSNPs))
        
    elif (nclusts >1 ) and (admixing) :
        nSNPs = cluster_frequencies.shape[1]
        genotypes = np.zeros((nsubjects, nSNPs))
        for i in range(nsubjects): 
            # Bias admixing proportion toward "reported race"
            admixture = np.repeat(1,nclusts)
            admixture[subject_ancestries[i]] = 2
            admixture = admixture / np.sum(admixture)
            genotypes[i,:] = sample_admixed_genotypes(seed, cluster_freqs = cluster_frequencies, admixture = admixture, nsubjects=1)
        
        
    # standardize the genotpyes
    freqs = np.mean(genotypes, axis=0) / 2
    # remove snps with frequencies of 0 or 1
    genotypes = genotypes[:, (freqs > 0.01) & (freqs < 0.99)]
    freqs = freqs[(freqs>0.01) & (freqs< 0.99)]
    stand_geno = np.matrix((genotypes- 2 * freqs) /
                          np.sqrt(2 * freqs * (1 - freqs)))

    # Calc standardized GRM
    GRM = np.dot(stand_geno, stand_geno.T) / nSNPs
    
    
    
    # project GRM onto pc space
    pcs = pd.DataFrame(PCA(n_components = 20).fit_transform(np.asarray(GRM)))
    pcs.columns = ["pc_" + str(col + 1) for col in pcs.columns]
    
    return genotypes, GRM, pcs

