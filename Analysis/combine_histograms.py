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

# with uproot.open('qcd2000.root') as file:
    
#     # j3_bin
#     j3_bin = hist.axis.Regular(label="Trijet Mass [GeV]", name="trijet_mass", bins=40, start=0, stop=6000)
#     j3_cat = hist.axis.StrCategory(label='Trijets', name='trijet', categories=["signal"])

#     j3_hist = Hist(j3_bin, j3_cat)
    
#     # j2_bin
#     j2_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=40, start=0, stop=4000)
#     j2_cat = hist.axis.StrCategory(label='Dijets', name='dijet', categories=["12 Pair","13 Pair","23 Pair"])

#     j2_hist = Hist(j2_bin, j2_cat)
    
#     # mjjs
#     mjj12_vs_mjjj = Hist(j3_bin,j2_bin)
#     mjj13_vs_mjjj = Hist(j3_bin,j2_bin)
#     mjj23_vs_mjjj = Hist(j3_bin,j2_bin)
    
#     # pNets
#     pNet_bin = hist.axis.Regular(label="pNet", name="pnet", bins=100, start=0, stop=1)
#     j1_pNet = Hist(pNet_bin)
#     j2_pNet = Hist(pNet_bin)
#     j3_pNet = Hist(pNet_bin)
    
#     for key in file.keys():
#         if 'j1_pNet' in key:
#             print(file[key].to_hist().values())
#             j1_pNet += file[key].to_hist()
#         if 'j2_pNet' in key:
#             j2_pNet.fill(pnet=file[key].to_hist().values())
#         if 'j3_pNet' in key:
#             j3_pNet.fill(pnet=file[key].to_hist().values())
            
#     plt.style.use([hep.style.CMS])
#     j1_pNet.plot()
#     hep.cms.text("Work in progress",loc=0)
#     plt.ylabel("Event count",horizontalalignment='right', y=1.0)
#     plt.legend()
#     plt.savefig("j1_pNet_QCD2000.png")
#     plt.cla()
#     plt.clf()

from os import listdir, getcwd, system
from os.path import isfile, join

list_of_root_files = []
for file in listdir(getcwd()):
    if not isfile(join(getcwd(), file)):
        continue
    if "qcd2000" in file:
        list_of_root_files.append(file)
        
system("hadd -f QCD2000.root {}".format(" ".join(list_of_root_files)))

with uproot.open("QCD2000.root") as file:
    plt.style.use([hep.style.CMS])
    file["j1_pNet"].to_hist().plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("QCD_j1_pNet.png")
    plt.cla()
    plt.clf()
    
    file["j2_pNet"].to_hist().plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("QCD_j2_pNet.png")
    plt.cla()
    plt.clf()
    
    file["j3_pNet"].to_hist().plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("QCD_j3_pNet.png")
    plt.cla()
    plt.clf()