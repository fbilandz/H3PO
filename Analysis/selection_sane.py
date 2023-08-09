import uproot
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import coffea.processor as processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import mplhep as hep
import ROOT 

def closest(masses):
    delta = abs(125 - masses)
    closest_masses = ak.min(delta, axis=1)
    is_closest = (delta == closest_masses)
    return is_closest

def HbbvsQCD(fatjet):
    score = (fatjet.particleNetMD_Xbb/(fatjet.particleNetMD_Xbb+fatjet.particleNetMD_QCD))
    return score


def applyKinematicCut(fatjets, ptcut = 250, etacut = 2.5, masscut = 50):
    return fatjets[(fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut) & (fatjets.msoftdrop>=masscut)]

def boosted_sane(fname,oFile,processLabel="signal",eventsToRead=None, n_of_tagged_jets=0):	
    try:
        events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset": "testSignal"},entry_stop=eventsToRead).events()
    except:
        print("Getting events failed for file: {}".format(fname))
        return [], [], [], [0, 0, 0, 0, 0, 0, 0, 0, 0], []
    
    froot = ROOT.TFile.Open(fname)
    myTree = froot.Runs
    for entry in myTree:
        total_events = entry.genEventCount

    fatjets = events.FatJet
    #Fatjet cuts
    ptcut = 250
    etacut = 2.5
    min_mass = 50
    
    total_skim_events = len(events)
    
    kin_good_fatjets = applyKinematicCut(fatjets, ptcut, etacut, min_mass)
    kin_pre_boosted_fatjets = kin_good_fatjets[ak.num(kin_good_fatjets, axis=1)> 2]
    # pre_boosted_events = events[ak.num(good_fatjets, axis=1)> 2]
    
    total_events_kin = len(kin_pre_boosted_fatjets)
    
    events_total = [total_events, total_skim_events, total_events_kin]
    
    return kin_pre_boosted_fatjets, events_total

def data_boosted_sane(fname,oFile,processLabel="signal",eventsToRead=None, n_of_tagged_jets=0):	
    try:
        events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset": "testSignal"},entry_stop=eventsToRead).events()
    except:
        print("Getting events failed for file: {}".format(fname))
        return [], [], [], [0, 0, 0, 0, 0, 0, 0, 0], []
    
    fatjets = events.FatJet
    #Fatjet cuts
    ptcut = 250
    etacut = 2.5
    min_mass = 50
    
    total_skim_events = len(events)
    
    kin_good_fatjets = applyKinematicCut(fatjets, ptcut, etacut, min_mass)
    kin_pre_boosted_fatjets = kin_good_fatjets[ak.num(kin_good_fatjets, axis=1)> 2]
    # pre_boosted_events = events[ak.num(good_fatjets, axis=1)> 2]
    
    total_events_kin = len(kin_pre_boosted_fatjets)
    
    events_total = [total_skim_events, total_events_kin]
    
    return kin_pre_boosted_fatjets, events_total

