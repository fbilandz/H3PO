import uproot
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import coffea.processor as processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema, schemas
import numpy as np
import mplhep as hep
from Selection import *
import ROOT

if __name__ == '__main__':
    j3_hist_1 = ROOT.TFile.Open("background/scaled/QCD17.root")
    print(j3_hist_1.Get("j3_hist").Integral())
    j3_hist_2 = ROOT.TFile.Open("background/scaled/TTbar17.root")
    print(j3_hist_2.Get("j3_hist").Integral())