from AdjHE.estimation.GCTA_wrapper import GCTA, gcta
from AdjHE.estimation.all_estimators import Basu_estimation
from Simulator.simulation_helpers.Sim_generator import pheno_simulator
import numpy as np
import pytest

#%% Basic testing for single site and cluster

@pytest.fixture
def C2S1() :
    rng = np.random.default_rng(123)
    sim = pheno_simulator(rng = rng, nsubjects= 1000)
    sim.sim_sites(nsites =1)
    sim.sim_pops(nclusts= 2)
    sim.sim_genos()
    sim.sim_pheno(h2Hom = 0.2, h2Het= [0.2, 0.6], alpha = 0)
    est = Basu_estimation()
    est.GRM = sim.GRM
    est.df = sim.df
    return est 

@pytest.mark.C2S1
def test_simNGCTA(C2S1) :
    est = C2S1
    result = est.estimate(mpheno = ["Y0"], npc = [0,1,2], Method = "GCTA", fixed_effects= ["Xc"])
    assert result["h2"][0] == pytest.approx(0.5, abs = 0.05) 

@pytest.mark.C2S1
def test_simAdjHE(C2S1):
    est = C2S1
    result = est.estimate(mpheno = ["Y0"], npc = [0,1,2], Method = "AdjHE", fixed_effects= ["Xc"])
    assert result["h2"][0] == pytest.approx(0.5, abs = 0.05) 

#%%
@pytest.mark.C2S1_thorough
def test_thoroughC1S1(C2S1): 
    est= C2S1
    df1= est.df.query("subj_ancestries==0")
    G1 = est.GRM[df1.index, :][:, df1.index]
    df2 = est.df.query("subj_ancestries==1")
    G2 = est.GRM[df2.index, :][:, df2.index]
    
    est1 = Basu_estimation()
    est1.GRM = G1
    est1.df = df1
    
    est2 = Basu_estimation()
    est2.GRM = G2
    est2.df = df2

    result1 = est1.estimate(mpheno = ["Y0"], npc = [0,1,2], Method = "GCTA", fixed_effects= ["Xc"])
    result2 = est2.estimate(mpheno = ["Y0"], npc = [0,1,2], Method = "GCTA", fixed_effects= ["Xc"])
