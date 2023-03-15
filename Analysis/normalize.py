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

def lumiNormalization(wp="tight",tagger="ParticleNet"):

    processes = ["QCD700","QCD1000","QCD1500","QCD2000","TTbarHadronic","TTbarSemileptonic"]
    for year in ['2017']:
        print(year, os.getcwd())
        nonScaledDir = os.getcwd() +  "/background/nonScaled"
        lumiScaledDir = os.getcwd() +  "/background/scaled"
        print(nonScaledDir)
        for proc in processes:
            nonScaledFile = "{0}/{1}.root".format(nonScaledDir,proc)
            if(os.path.isfile(nonScaledFile)):
                try:                 
                    normalizeProcess(proc,year,"{0}/{1}_atleast_2b-tagged.root".format(nonScaledDir,proc),"{0}/{1}.root".format(lumiScaledDir,proc))
                except:
                    print("Couldn't normalize {0}".format(proc))
            else:
                print("{0} does not exist, skipping!".format(nonScaledFile))
        
        QCDsamples = ["QCD700.root","QCD1000.root","QCD1500.root","QCD2000.root"]
        QCDsamples = [os.path.join(lumiScaledDir, f) for f in QCDsamples if (os.path.isfile(os.path.join(lumiScaledDir, f)))]
        mergeSamples(QCDsamples,"{0}/QCD{1}_atleast_2b-tagged.root".format(lumiScaledDir,year[2:]),"QCD\d+_","QCD_")

        ttSamples = ["TTbarHadronic.root","TTbarSemileptonic.root"]
        ttSamples = [os.path.join(lumiScaledDir, f) for f in ttSamples if (os.path.isfile(os.path.join(lumiScaledDir, f)))]
        mergeSamples(ttSamples,"{0}/TTbar{1}_atleast_2b-tagged.root".format(lumiScaledDir,year[2:]),"TTbarSemileptonic|TTbarHadronic","TTbar")

        # JetHTSamples = [nonScaledDir+f for f in os.listdir(nonScaledDir) if (os.path.isfile(os.path.join(nonScaledDir, f)) and "JetHT" in f)]
        # mergeSamples(JetHTSamples,"{0}/JetHT{1}.root".format(lumiScaledDir,year[2:]),"JetHT201[0-9][a-zA-Z]+_","data_obs_")


if __name__ == '__main__':

    #lumiNormalization(wp="tight")    
    #lumiNormalization(wp="medium")    
    #lumiNormalization(wp="loose")

    # lumiNormalization(wp="tight",tagger="DeepDoubleX")
    # lumiNormalization(wp="tight",tagger="DeepAK8")
    # lumiNormalization(wp="tight",tagger="Hbb")    
    lumiNormalization(wp="loose",tagger="/")
