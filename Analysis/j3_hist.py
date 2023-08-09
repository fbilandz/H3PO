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

with uproot.open("background/scaled/QCD17.root") as file:
    print(file.keys())
    j3_hist = file["j3_hist;1"].to_hist()
    
    plt.style.use([hep.style.CMS])
    j3_hist.plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j3_hist_QCD.png")
    plt.cla()
    plt.clf()
    
    mjjall_vs_mjjj = file["mjjall_vs_mjjj"].to_hist()
    mjjall_vs_mjjj.plot()
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("mjjall_vs_mjj_QCD.png")
    plt.cla()
    plt.clf()
    
    j1_pNet = file["j1_pNet"].to_hist()
    plt.yscale('log')
    j1_pNet.plot()
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j1_pNet_QCD.png")
    plt.cla()
    plt.clf()
    
    j2_pNet = file["j2_pNet"].to_hist()
    plt.yscale('log')
    j2_pNet.plot()
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j2_pNet_QCD.png")
    plt.cla()
    plt.clf()
    
    j3_pNet = file["j3_pNet"].to_hist()
    plt.yscale('log')
    j3_pNet.plot()
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j3_pNet_QCD.png")
    plt.cla()
    plt.clf()
    
with uproot.open("background/scaled/TTbar17.root") as file:
    print(file.keys())
    j3_hist = file["j3_hist;1"].to_hist()
    
    plt.style.use([hep.style.CMS])
    j3_hist.plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j3_hist_TTbar.png")
    plt.cla()
    plt.clf()
    
    mjjall_vs_mjjj = file["mjjall_vs_mjjj"].to_hist()
    mjjall_vs_mjjj.plot()
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("mjjall_vs_mjj_TTbar.png")
    plt.cla()
    plt.clf()
    
    j1_pNet = file["j1_pNet"].to_hist()
    plt.yscale('log')
    j1_pNet.plot()
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j1_pNet_TTbar.png")
    plt.cla()
    plt.clf()
    
    j2_pNet = file["j2_pNet"].to_hist()
    plt.yscale('log')
    j2_pNet.plot()
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j2_pNet_TTbar.png")
    plt.cla()
    plt.clf()
    
    j3_pNet = file["j3_pNet"].to_hist()
    plt.yscale('log')
    j3_pNet.plot()
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j3_pNet_TTbar.png")
    plt.cla()
    plt.clf()
    
with uproot.open("background/scaled/TTbar17_loose.root") as file:
    print(file.keys())
    j3_hist = file["j3_hist;1"].to_hist()
    
    plt.style.use([hep.style.CMS])
    j3_hist.plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j3_hist_TTbar_loose.png")
    plt.cla()
    plt.clf()
    
with uproot.open("background/scaled/QCD17_loose.root") as file:
    print(file.keys())
    j3_hist = file["j3_hist;1"].to_hist()
    
    plt.style.use([hep.style.CMS])
    j3_hist.plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("j3_hist_QCD_loose.png")
    plt.cla()
    plt.clf()