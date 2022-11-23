import uproot
import awkward as ak
from coffea.nanoevents import NanoEventsFactory, BaseSchema, NanoAODSchema
import numpy as np
import ROOT as r
from optparse import OptionParser
import os
import time

def is_rootcompat(a):
    """Is it a flat or 1-d jagged array?"""
    t = ak.type(a)
    if isinstance(t, ak._ext.ArrayType):
        if isinstance(t.type, ak._ext.PrimitiveType):
            return True
        if isinstance(t.type, ak._ext.ListType) and isinstance(t.type.type, ak._ext.PrimitiveType):
            return True
    return False

def uproot_writeable(events):
    """Restrict to columns that uproot can write compactly"""
    out = {}
    for bname in events.fields:
        if events[bname].fields:
            out[bname] = ak.zip(
                {
                    n: ak.packed(ak.without_parameters(events[bname][n]))
                    for n in events[bname].fields
                    if is_rootcompat(events[bname][n])
                }
            )
        else:
            out[bname] = ak.packed(ak.without_parameters(events[bname]))
    return out

def skim(inputFile,outputFile,eventsToRead=None):
    print("Skimming {0}".format(inputFile))
    events = NanoEventsFactory.from_root(inputFile,schemaclass=NanoAODSchema,entry_stop=eventsToRead).events()
    ptCut  = 200
    msdCut = 50
    etaCut = 2.5

    ptMask       = events.FatJet.pt>ptCut
    msdMask      = events.FatJet.msoftdrop>msdCut
    etaMask      = np.abs(events.FatJet.eta)<etaCut

    #We require at least two FatJets satisfying pt, eta and msd requirements
    #This allows for 3+0 or 2+1 (AK8Jet+AK4Jet topologies)
    skimmingMask = ak.sum(ptMask & msdMask & etaMask, axis=1)>1
    skimmed      = events[skimmingMask]
    with uproot.recreate(outputFile) as fout:
        fout["Events"] = uproot_writeable(skimmed)

def copyRunsTree(inputFile,outputFile):
    print("Storing Runs tree in {0}".format(outputFile))
    #Save Runs tree
    #Copying TTrees with uproot is not yet supported so we use ROOT directly
    inputFile  = r.TFile.Open(inputFile)
    runsTree   = inputFile.Get("Runs")
    outputFile = r.TFile.Open(outputFile,"UPDATE")
    outputFile.cd()
    runsTree.CloneTree().Write()
    outputFile.Close()
    inputFile.Close()

def localCopy(inputLFN):
    xrdcpCMD = "xrdcp root://cms-xrd-global.cern.ch//{0} .".format(inputLFN)
    print(xrdcpCMD)
    os.system(xrdcpCMD)

parser = OptionParser()
parser.add_option('-i', '--input', metavar='IFILE', type='string', action='store',
                default   =   '',
                dest      =   'input',
                help      =   'A root file or text file with multiple root file locations to analyze')
parser.add_option('-o', '--odir', metavar='ODIR', type='string', action='store',
                default   =   '',
                dest      =   'outputDir',
                help      =   'Output directory path.')
    
(options, args) = parser.parse_args()
start_time      = time.time()

if(".txt" in options.input):
    inputFiles  = open(options.input, 'r')
    lines       = inputFiles.readlines()
    for iFile in lines:
        iFile    = iFile.rstrip()#Remove trailing newline
        localCopy(iFile)
        fileName = iFile.split("/")[-1]
        odir = options.outputDir
        if not os.path.exists(odir):
            print("CREATING DIR: ", odir)
            os.makedirs(odir)

        skim(fileName,"{0}/{1}".format(odir,fileName),eventsToRead=None)
        copyRunsTree(fileName,"{0}/{1}".format(odir,fileName))
        print("Removing local file {0}".format(fileName))
        os.system("rm {0}".format(fileName))


else:
    localCopy(options.input)
    fileName = options.input.split("/")[-1]
    odir = options.outputDir
    if not os.path.exists(odir):
        print("CREATING DIR: ", odir)
        os.makedirs(odir)

    skim(fileName,"{0}/{1}".format(odir,fileName),eventsToRead=None)
    copyRunsTree(fileName,"{0}/{1}".format(odir,fileName))
    print("Removing local file {0}".format(fileName))
    os.system("rm {0}".format(fileName))
    
print ('%s sec'%(time.time()-start_time))
