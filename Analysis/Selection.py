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

def closest(masses):
    delta = abs(125 - masses)
    closest_masses = ak.min(delta, axis=1)
    is_closest = (delta == closest_masses)
    return is_closest

def HbbvsQCD(fatjet):
    score = (fatjet.particleNetMD_Xbb/(fatjet.particleNetMD_Xbb+fatjet.particleNetMD_QCD))
    return score

def boosted(fname,oFile,processLabel="signal",eventsToRead=None):	
    try:
        events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset": "testSignal"},entry_stop=eventsToRead).events()
    except:
        print("Getting events failed for file: {}".format(fname))
        return [], 0, 0
    
    fatjets = events.FatJet
    
    #Fatjet cuts
    ptcut = 250
    etacut = 2.5
    mass_cut = [100,150]
    pNet_cut = 0.0

    good_fatjets = fatjets[(fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut) & (fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])]
    pre_boosted_fatjets = good_fatjets[ak.num(good_fatjets, axis=1)> 2]
    pre_boosted_events = events[ak.num(good_fatjets, axis=1)> 2]
    #Btag cut applied at the end
    btag_boosted = pre_boosted_fatjets[HbbvsQCD(pre_boosted_fatjets)>=pNet_cut]
    btag_boosted_fatjets = btag_boosted[ak.num(btag_boosted, axis=1)> 2]
    btag_boosted_events = pre_boosted_events[ak.num(btag_boosted, axis=1)> 2]

    return btag_boosted_fatjets, len(events), len(btag_boosted_events)

def semiboosted(fname,oFile,processLabel="signal",eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset": "testSignal"},entry_stop=eventsToRead).events()

    fatjets = events.FatJet

    ##FatJet cuts
    ptcut = 250
    etacut = 2.5
    mass_cut = [100,150]
    pNet_cut = 0.9105
    
    good_fatjets = fatjets[(fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut) & (fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])]
    pre_semiboosted_fatjets = good_fatjets[ak.num(good_fatjets, axis=1) == 2]
    pre_semiboosted_events = events[ak.num(good_fatjets, axis=1) == 2]
    #Btag cut for fatjets applied after pre selection
    btag_semiboosted = pre_semiboosted_fatjets[HbbvsQCD(pre_semiboosted_fatjets)>=pNet_cut]
    btag_semiboosted_fatjets = btag_semiboosted[ak.num(btag_semiboosted, axis=1) == 2]
    btag_semiboosted_events = pre_semiboosted_events[ak.num(btag_semiboosted, axis=1) == 2]
    
    #Resolved jet cuts
    res_ptcut = 30
    res_etacut = 2.5
    res_mass_cut = [90,150]
    # loose cut = 0.0532, med_cut = 0.3040, tight_cut = 0.7476 , https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17   
    res_deepBcut = 0.0532

    #getting jets from selected fatjet events
    res_jets = btag_semiboosted_events.Jet

    good_pre_jets = res_jets[(res_jets.pt > res_ptcut) & (np.absolute(res_jets.eta) < res_etacut) & (res_jets.btagDeepB>res_deepBcut)]
    #Applying selection to all objects
    good_semiboosted_jets = good_pre_jets[ak.num(good_pre_jets)>1]
    good_semiboosted_fatjets = btag_semiboosted_fatjets[ak.num(good_pre_jets)>1]
    good_semiboosted_events = btag_semiboosted_events[ak.num(good_pre_jets)>1]
    
    #veto jets overlaping with fatjet
    good_pairs = good_semiboosted_jets.nearest(good_semiboosted_fatjets).delta_r(good_semiboosted_jets)>0.8
    good_paired_jets = good_semiboosted_jets[good_pairs]
    
    #make sure there are atleast 2 selected resolved jets in an event
    min_paired_jets = good_paired_jets[ak.num(good_paired_jets, axis=1) >= 2]
    min_paired_fatjets = good_semiboosted_fatjets[ak.num(good_paired_jets, axis=1) >= 2]
    min_paired_events = good_semiboosted_events[ak.num(good_paired_jets, axis=1) >= 2]

    #selecting jet pair whose mass is closest to Higgs mass
    dijets = ak.combinations(min_paired_jets, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]
    mass_jets = closest_dijets[((closest_dijets['i0'] + closest_dijets['i1']).mass>=res_mass_cut[0]) & ((closest_dijets['i0'] + closest_dijets['i1']).mass<=res_mass_cut[1])]
    selected_jets = mass_jets[ak.num(mass_jets,axis=1)>0]
    selected_fatjets = min_paired_fatjets[ak.num(mass_jets,axis=1)>0]
    selected_events = min_paired_events[ak.num(mass_jets,axis=1)>0]

    return selected_fatjets,selected_jets
