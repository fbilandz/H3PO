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

def plotMassDist(fname,oFile,processLabel="signal",eventsToRead=None):	
	events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset": "testSignal"},entry_stop=eventsToRead).events()


	ptcut  = 250
	etacut = 2.5

	fatjets = events.FatJet[(events.FatJet.pt>ptcut) & (np.abs(events.FatJet.eta)<etacut)]
	trijets = fatjets[(ak.num(fatjets, axis=1) > 2)]


	#-----MJJJ calc and plotting-----#

	trijet_mass = (trijets[:,0]+trijets[:,1]+trijets[:,2]).mass
	#calc inv mass of trijets by lorentz v. sum of three leading jets


	j3_bin = hist.axis.Regular(label="Trijet Mass [GeV]", name="trijet_mass", bins=40, start=0, stop=4000)
	j3_cat = hist.axis.StrCategory(label='Trijets', name='trijet', categories=[processLabel])#can add bkg categories later on

	j3_hist = Hist(j3_bin, j3_cat)
	j3_hist.fill(trijet=processLabel, trijet_mass=trijet_mass)

	plt.style.use([hep.style.CMS])
	j3_hist.plot(color="black")
	hep.cms.text("Work in progress",loc=0)
	plt.ylabel("Event count",horizontalalignment='right', y=1.0)
	plt.legend()
	plt.savefig("MJJJ_{0}.png".format(oFile))
	plt.cla()
	plt.clf()

	#-----MJJ calc and plotting-----#


	dijet1_mass = (trijets[:,0]+trijets[:,1]).mass
	#calc inv mass of first dijet combination

	dijet2_mass = (trijets[:,0]+trijets[:,2]).mass
	#calc inv mass of second dijet combination

	dijet3_mass = (trijets[:,1]+trijets[:,2]).mass
	#calc inv mass of third dijet combination


	j2_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=40, start=0, stop=2000)
	j2_cat = hist.axis.StrCategory(label='Dijets', name='dijet', categories=["12 Pair","13 Pair","23 Pair"])

	j2_hist = Hist(j2_bin, j2_cat)

	j2_hist.fill(dijet="12 Pair", dijet_mass=dijet1_mass)
	j2_hist.fill(dijet="13 Pair", dijet_mass=dijet2_mass)
	j2_hist.fill(dijet="23 Pair", dijet_mass=dijet3_mass)


	j2_hist.plot(stack=True,histtype='fill',ec="black",fc=["violet","skyblue","khaki"])
	hep.cms.text("Work in progress",loc=0)
	plt.ylabel("Event count",horizontalalignment='right', y=1.0)
	plt.legend()
	plt.savefig("MJJ_{0}.png".format(oFile))
	print("Saved MJJ_{0}.png".format(oFile))
	plt.cla()
	plt.clf()


fname   = "/STORE/ferencek/TRSM_XToHY_6b/2017/13TeV/NANOAOD/TRSM_XToHY_6b_M3_2000_M2_1100_NANOAOD.root"

MX = [2000,2400,2800,3200,3600,4000]
MY = [700,1100,1500]

for mx in MX:
	for my in MY:
		fname   = "/STORE/ferencek/TRSM_XToHY_6b/2017/13TeV/NANOAOD/TRSM_XToHY_6b_M3_{0}_M2_{1}_NANOAOD.root".format(mx,my)
		oFile   = "{0}_{1}".format(mx,my)
		plotMassDist(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)