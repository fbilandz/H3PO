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

def combine_histograms(dataset, wp="none"):
    SKIM_DIR = "/STORE/matej/H3_skims/2017/QCD1000"
    list_of_root_files = []

    for file in listdir(SKIM_DIR):
        if not isfile(join(SKIM_DIR, file)):
            continue
        if '.root' in file and '.png' not in file:
            list_of_root_files.append(join(SKIM_DIR, file))
    print(list_of_root_files)

    system("hadd -f {0}_{1}.root {2}".format("QCD1000", "Other", " ".join(list_of_root_files)))
    # system("mv {0}_{1}.root ./background/nonScaled/".format(dataset, wp))

if __name__ == '__main__':
    combine_histograms("QCD")