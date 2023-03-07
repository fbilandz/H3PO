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
from os import listdir, getcwd, system
from os.path import isfile, join

with uproot.open("QCD1000.root") as file:
    print(file.keys())
    j3_hist = file["j3_hist;1"].to_hist()
    
    plt.style.use([hep.style.CMS])
    j3_hist.plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j3_hist_QCD1000.png")
    plt.cla()
    plt.clf()