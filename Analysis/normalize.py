import ROOT as r
import json
import sys
import re
import os

def normalizeProcess(process,year,inFile,outFile):
    h_dict = {}
    f = r.TFile.Open(inFile)
    print(process,inFile)
    json_file = open("xsecs.json")
    config = json.load(json_file)
    xsec    = config[year][process]["xsec"]
    luminosity  = config[year]["lumi"]
    sumGenW     = f.Get("events_total").GetBinContent(1)
    nLumi       = xsec*luminosity
    scaling     = nLumi/sumGenW
    print("Scale: {0:.6f}".format(scaling))
    for key in f.GetListOfKeys():
        h = key.ReadObj()
        hName = h.GetName()
        h.Scale(scaling)
        h.SetDirectory(0)
        h_dict[hName] = h
    f.Close()

    f = r.TFile(outFile,"recreate")
    f.cd()
    for key in h_dict:
        histo = h_dict[key]
        histo.Write()
    f.Close()

def mergeSamples(inFiles,outFile,regexMatch,regexReplace):
    h_dict = {}
    print("Merging to {0}".format(outFile))
    for inFile in inFiles:
        print(inFile)
        f        = r.TFile.Open(inFile) 
        for key in f.GetListOfKeys():
            h = key.ReadObj()
            hName = h.GetName()
            h.SetDirectory(0)
            hKey = re.sub(regexMatch,regexReplace,hName,count=1)
            if not hKey in h_dict:
                h.SetName(hKey)
                h_dict[hKey] = h
            else:
                h_dict[hKey].Add(h)
        f.Close()
    f = r.TFile(outFile,"recreate")
    f.cd()
    for key in h_dict:
        histo = h_dict[key]
        histo.Write()
    f.Close()
    print("\n")

def lumi_normalization(wp="tight",tagger="ParticleNet", n_of_tagged_jets=1):
    print("N of tagged jets: ", n_of_tagged_jets)
    processes = ["QCD500", "QCD700","QCD1000","QCD1500","QCD2000","TTbarHadronic","TTbarSemileptonic"]
    for year in ['2017']:
        print(year, os.getcwd())
        nonScaledDir = os.getcwd() +  "/background/nonScaled"
        lumiScaledDir = os.getcwd() +  "/background/scaled"
        print(nonScaledDir)
        for proc in processes:
            nonScaledFile = "{0}/{1}_{2}b-tagged_jets.root".format(nonScaledDir,proc, n_of_tagged_jets)
            if(os.path.isfile(nonScaledFile)):
                try:                 
                    normalizeProcess(proc,year,"{0}/{1}_{2}b-tagged_jets.root".format(nonScaledDir,proc, n_of_tagged_jets),"{0}/{1}_{2}b-tagged_jets.root".format(lumiScaledDir,proc, n_of_tagged_jets))
                except:
                    print("Couldn't normalize {0}".format(proc))
            else:
                print("{0} does not exist, skipping!".format(nonScaledFile))
        
        QCDsamples = ["QCD500", "QCD700","QCD1000","QCD1500","QCD2000"]
        QCDsamples = [os.path.join(lumiScaledDir, f + "_{0}b-tagged_jets.root".format(n_of_tagged_jets)) for f in QCDsamples if (os.path.isfile(os.path.join(lumiScaledDir, f + "_{0}b-tagged_jets.root".format(n_of_tagged_jets))))]
        mergeSamples(QCDsamples,"{0}/QCD{1}_{2}_b-tag.root".format(lumiScaledDir,year[2:], n_of_tagged_jets),"QCD\d+_","QCD_")

        ttSamples = ["TTbarHadronic","TTbarSemileptonic"]
        ttSamples = [os.path.join(lumiScaledDir, f + "_{0}b-tagged_jets.root".format(n_of_tagged_jets)) for f in ttSamples if (os.path.isfile(os.path.join(lumiScaledDir, f + "_{0}b-tagged_jets.root".format(n_of_tagged_jets))))]
        mergeSamples(ttSamples,"{0}/TTbar{1}_{2}_b-tag.root".format(lumiScaledDir,year[2:], n_of_tagged_jets),"TTbarSemileptonic|TTbarHadronic","TTbar")

        JetHTSamples = ["JetHT2017B", "JetHT2017C", "JetHT2017D", "JetHT2017E", "JetHT2017F"]
        JetHTSamples = [os.path.join(nonScaledDir, f + "_{0}b-tagged_jets.root".format(n_of_tagged_jets)) for f in JetHTSamples if (os.path.isfile(os.path.join(nonScaledDir, f + "_{0}b-tagged_jets.root".format(n_of_tagged_jets))))]
        mergeSamples(JetHTSamples,"{0}/JetHT{1}_{2}_b-tag.root".format(lumiScaledDir,year[2:], n_of_tagged_jets),"JetHT201[0-9][a-zA-Z]+_","data_obs_")


if __name__ == '__main__':

    #lumiNormalization(wp="tight")    
    #lumiNormalization(wp="medium")    
    #lumiNormalization(wp="loose")

    # lumiNormalization(wp="tight",tagger="DeepDoubleX")
    # lumiNormalization(wp="tight",tagger="DeepAK8")
    # lumiNormalization(wp="tight",tagger="Hbb")    
    lumi_normalization(wp="loose",tagger="/")
