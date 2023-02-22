# Files:
skimming.py - perform a loose selection on the files and store "skimmed" files. Execution time of the selection script is significantly reduced if skims are used as input\
Selection.py - implements all the selection\
Efficiency_plot.py - creates 2D efficiency plot (Mass Y vs. Mass X)\
mass_matching_plots_boosted.py - creates MJJJ and MJJ mass distributions for boosted events\
mass_matching_plots_semiboosted.py - creates MJJJ and MJJ mass distributions for semiboosted events\
HHH_samples_2016.txt - Official sample list of 2016 NanoAOD XToYHTo6B samples (Needs to copy to Lorien once production is complete)\
HHH_samples_2017.txt - Official sample list of 2017 NanoAOD XToYHTo6B samples (Needs to copy to Lorien once production is complete)

# Example commands:
Grid proxy needs to be initialized before running skimming to access the file on the store
```
python skimming.py -i store/mc/RunIISummer20UL17NanoAODv9/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v1/100000/D5426269-CD07-CA4C-8E9E-E2336514139F.root -o test_output
```
