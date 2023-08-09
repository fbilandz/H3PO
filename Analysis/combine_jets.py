from condor.paths import *
datasets = ["QCD1500"]

# for file in dataset:
#     f_test2 = ROOT.TFile(file)

from os import listdir, system
from os.path import join, isfile

listofpaths = []
for dataset in datasets:
    dataset_path = join(SKIM_DIR, '2017', dataset)
    
    for file in listdir(dataset_path):
        file_path = join(dataset_path, file)
        if not isfile(file_path):
            continue
        listofpaths.append(file_path)
system("hadd -f QCD1500.root {0}".format(" ".join(listofpaths)))
        
        