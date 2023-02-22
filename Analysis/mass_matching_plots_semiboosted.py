import uproot
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import coffea.processor as processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import mplhep as hep
from Selection import *

def plotMassDist(fname,oFile,processLabel="signal",eventsToRead=None):	

    semiboosted_selection = semiboosted(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)
    selected_fatjets = semiboosted_selection[0]
    selected_jets = semiboosted_selection[1]


    #-----MJJJ calc and plotting-----#

    tri_mass = (selected_fatjets[:,0]+selected_fatjets[:,1]+selected_jets['i0']+selected_jets['i1']).mass
    trijet_mass = []
    for t in tri_mass:
        for i in t:
            trijet_mass.append(i)


    j3_bin = hist.axis.Regular(label="Trijet Mass [GeV]", name="trijet_mass", bins=40, start=0, stop=6000)
    j3_cat = hist.axis.StrCategory(label='Trijets', name='trijet', categories=[processLabel])#can add bkg categories later on

    j3_hist = Hist(j3_bin, j3_cat)
    j3_hist.fill(trijet=processLabel, trijet_mass=trijet_mass)

    plt.style.use([hep.style.CMS])
    j3_hist.plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("semiBoosted_MJJJ_{0}.png".format(oFile))
    plt.cla()
    plt.clf()

    #-----MJJ calc and plotting-----#


    dijet1_mass = (selected_fatjets[:,0]+selected_fatjets[:,1]).mass
    di2_mass = (selected_fatjets[:,0]+selected_jets['i0']+selected_jets['i1']).mass
    di3_mass = (selected_fatjets[:,1]+selected_jets['i0']+selected_jets['i1']).mass
    dijet2_mass = []
    dijet3_mass = []

    for d2 in di2_mass:
        for m2 in d2:
            dijet2_mass.append(m2)
    for d3 in di3_mass:
        for m3 in d3:
            dijet3_mass.append(m3)

    j2_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=40, start=0, stop=4000)
    j2_cat = hist.axis.StrCategory(label='Dijets', name='dijet', categories=["12 Pair","13 Pair","23 Pair"])

    j2_hist = Hist(j2_bin, j2_cat)

    j2_hist.fill(dijet="12 Pair", dijet_mass=dijet1_mass)
    j2_hist.fill(dijet="13 Pair", dijet_mass=dijet2_mass)
    j2_hist.fill(dijet="23 Pair", dijet_mass=dijet3_mass)


    j2_hist.plot(stack=True,histtype='fill',ec="black",fc=["violet","skyblue","khaki"])
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("semiBoosted_MJJ_{0}.png".format(oFile))
    print("Saved MJJ_{0}.png".format(oFile))
    plt.cla()
    plt.clf()

fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_2000_M2_1100_NANOAOD.root"

MX = [400,800,1200,1600,2000,2400,2800,3200,3600,4000]
MY = [260,300,700,1100,1500,1900,2300,2700,3100,3500,3900]

for mx in MX:
    for my in MY:
        if my+130<mx:
            fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_{0}_M2_{1}_NANOAOD.root".format(mx,my)
            oFile   = "{0}_{1}".format(mx,my)
            plotMassDist(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)

        elif my+100==mx:
            my = my-40
            fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_{0}_M2_{1}_NANOAOD.root".format(mx,my)
            oFile   = "{0}_{1}".format(mx,my)
            plotMassDist(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)
