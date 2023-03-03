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


def plotMassDist(fname,oFile,processLabel="signal",eventsToRead=None):

    good_boosted = boosted(fname,oFile,processLabel="JetHT_BACKGROUND",eventsToRead=None)
    print(good_boosted)
    if len(good_boosted) == 0:
        return
    trijet_mass = (good_boosted[:,0]+good_boosted[:,1]+good_boosted[:,2]).mass
    #calc inv mass of trijets by lorentz v. sum of three leading jets

    j3_bin = hist.axis.Regular(label="Trijet Mass [GeV]", name="trijet_mass", bins=40, start=0, stop=6000)
    j3_cat = hist.axis.StrCategory(label='Trijets', name='trijet', categories=[processLabel])

    j3_hist = Hist(j3_bin, j3_cat)
    j3_hist.fill(trijet=processLabel, trijet_mass=trijet_mass)

    plt.style.use([hep.style.CMS])
    j3_hist.plot(color="black")
    hep.cms.text("Work in progress",loc=0)
    plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("MJJJ_btag_{0}.png".format(oFile))
    plt.cla()
    plt.clf()

    #-----MJJ calc and plotting-----#


    dijet1_mass = (good_boosted[:,0]+good_boosted[:,1]).mass
    #calc inv mass of first dijet combination

    dijet2_mass = (good_boosted[:,0]+good_boosted[:,2]).mass
    #calc inv mass of second dijet combination

    dijet3_mass = (good_boosted[:,1]+good_boosted[:,2]).mass
    #calc inv mass of third dijet combination


    j2_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=40, start=0, stop=4000)
    j2_cat = hist.axis.StrCategory(label='Dijets', name='dijet', categories=["12 Pair","13 Pair","23 Pair"])

    j2_hist = Hist(j2_bin, j2_cat)

    j2_hist.fill(dijet="12 Pair", dijet_mass=dijet1_mass)
    j2_hist.fill(dijet="13 Pair", dijet_mass=dijet2_mass)
    j2_hist.fill(dijet="23 Pair", dijet_mass=dijet3_mass)


    j2_hist.plot(stack=True, histtype='fill', ec="black", fc=["violet","skyblue","khaki"])
    hep.cms.text("Work in progress", loc=0)
    plt.ylabel("Event count", horizontalalignment='right', y=1.0)
    plt.legend()
    plt.savefig("MJJ_btag_{0}.png".format(oFile))
    print("Saved MJJ_btag_{0}.png".format(oFile))
    plt.cla()
    plt.clf()


#fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_2000_M2_1100_NANOAOD.root" #(on lxplus)
fname = "/STORE/matej/H3_skims/2017/TTbarSemileptonic/" 

from os import listdir
from os.path import isfile, join
for file in listdir(fname):
    if not isfile(join(fname, file)):
        continue
    plotMassDist(join(fname, file), "TTbar{0}".format(file), processLabel="TTbar", eventsToRead=None)


