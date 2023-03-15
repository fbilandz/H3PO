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

def remove_root_files(list_of_root_files):
    for file in list_of_root_files:
        system('rm ' + file)

def combine_histograms(dataset, wp="none"):
    
    list_of_root_files = []
    try:
        system('rm {0}_{1}.root'.format(dataset, wp))
    except:
        print('{0}_{1}.root didn\'t exist before'.format(dataset, wp))
        
    for file in listdir(getcwd()):
        if not isfile(join(getcwd(), file)):
            continue
        if dataset in file and '.root' in file and '.png' not in file:
            list_of_root_files.append(file)
            
    system("hadd -f {0}_{1}.root {2}".format(dataset, wp, " ".join(list_of_root_files)))
    remove_root_files(list_of_root_files)
    
    with uproot.open("{0}_{1}.root".format(dataset, wp)) as file:
        plt.style.use([hep.style.CMS])
        file["j1_pNet"].to_hist().plot(color="black")
        hep.cms.text("Work in progress",loc=0)
        plt.ylabel("Event count",horizontalalignment='right', y=1.0)
        plt.yscale('log')
        plt.legend()
        plt.savefig("{0}_{1}_j1_pNet.png".format(dataset, wp))
        plt.cla()
        plt.clf()
        
        file["j2_pNet"].to_hist().plot(color="black")
        hep.cms.text("Work in progress",loc=0)
        plt.ylabel("Event count",horizontalalignment='right', y=1.0)
        plt.legend()
        plt.savefig("{0}_{1}_j2_pNet.png".format(dataset, wp))
        plt.cla()
        plt.clf()
        
        file["j3_pNet"].to_hist().plot(color="black")
        hep.cms.text("Work in progress",loc=0)
        plt.ylabel("Event count",horizontalalignment='right', y=1.0)
        plt.legend()
        plt.savefig("{0}_{1}_j3_pNet.png".format(dataset, wp))
        plt.cla()
        plt.clf()