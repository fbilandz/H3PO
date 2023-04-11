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
from Selection import boosted, HbbvsQCD


def plotMassDist(fname,oFile,processLabel="signal",eventsToRead=None, n_of_tagged_jets=0):

    good_boosted, total_events, control_good_boosted, control_total_selected_events, control_alternative_good_boosted, control_alternative_total_selected_events = boosted(fname,oFile,processLabel="JetHT_BACKGROUND",eventsToRead=None, n_of_tagged_jets=n_of_tagged_jets)

    print(good_boosted[:,0])
    
    trijet_mass = (good_boosted[:,0]+good_boosted[:,1]+good_boosted[:,2]).mass
    print(trijet_mass)
    #calc inv mass of trijets by lorentz v. sum of three leading jets

    j3_bin = hist.axis.Regular(label="Trijet Mass [GeV]", name="trijet_mass", bins=60, start=0, stop=6000)
    # j3_cat = hist.axis.StrCategory(label='Trijets', name='trijet', categories=[processLabel])

    j3_hist = Hist(j3_bin)
    j3_hist.fill(trijet_mass=trijet_mass)
    j1_mass = good_boosted[:,0].msoftdrop
    j2_mass = good_boosted[:,1].msoftdrop
    j3_mass = good_boosted[:,2].msoftdrop
    
    j1_mass_control = control_good_boosted[:,0].msoftdrop
    j2_mass_control = control_good_boosted[:,1].msoftdrop
    j3_mass_control = control_good_boosted[:,2].msoftdrop
    
    j1_mass_control_alternative = control_alternative_good_boosted[:,0].msoftdrop
    j2_mass_control_alternative = control_alternative_good_boosted[:,1].msoftdrop
    j3_mass_control_alternative = control_alternative_good_boosted[:,2].msoftdrop
    # plt.style.use([hep.style.CMS])
    # j3_hist.plot(color="black")
    # hep.cms.text("Work in progress",loc=0)
    # plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    # plt.legend()
    # plt.savefig("MJJJ_btag_{0}.png".format(oFile))
    # plt.cla()
    # plt.clf()

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

    mjj12_vs_mjjj = Hist(j3_bin,j2_bin)
    mjj12_vs_mjjj.fill(dijet_mass=dijet1_mass,trijet_mass=trijet_mass)
    mjj13_vs_mjjj = Hist(j3_bin,j2_bin)
    mjj13_vs_mjjj.fill(dijet_mass=dijet2_mass,trijet_mass=trijet_mass)
    mjj23_vs_mjjj = Hist(j3_bin,j2_bin)
    mjj23_vs_mjjj.fill(dijet_mass=dijet3_mass,trijet_mass=trijet_mass)
    
    mjjall_vs_mjjj = Hist(j3_bin, j2_bin)
    mjjall_vs_mjjj.fill(dijet_mass=dijet1_mass,trijet_mass=trijet_mass)
    mjjall_vs_mjjj.fill(dijet_mass=dijet2_mass,trijet_mass=trijet_mass)
    mjjall_vs_mjjj.fill(dijet_mass=dijet3_mass,trijet_mass=trijet_mass)
    
    events_cat  = hist.axis.Integer(0, 6, underflow=False, overflow=False)
    events_total = Hist(events_cat)
    events_total[0] = total_events[0]
    events_total[1] = total_events[1]
    events_total[2] = total_events[2]
    events_total[3] = total_events[3]
    events_total[4] = control_total_selected_events
    events_total[5] = control_alternative_total_selected_events

    # j2_hist.plot(stack=True, histtype='fill', ec="black", fc=["violet","skyblue","khaki"])
    # hep.cms.text("Work in progress", loc=0)
    # plt.ylabel("Event count", horizontalalignment='right', y=1.0)
    # plt.legend()
    # plt.savefig("MJJ_btag_{0}.png".format(oFile))
    # print("Saved MJJ_btag_{0}.png".format(oFile))
    # plt.cla()
    # plt.clf()
    
    pNet_bin = hist.axis.Regular(label="pNet", name="pnet", bins=100, start=0, stop=1)
    j1_pNet = Hist(pNet_bin)
    j2_pNet = Hist(pNet_bin)
    j3_pNet = Hist(pNet_bin)
    j1_pNet.fill(pnet=HbbvsQCD(good_boosted[:,0]))
    j2_pNet.fill(pnet=HbbvsQCD(good_boosted[:,1]))
    j3_pNet.fill(pnet=HbbvsQCD(good_boosted[:,2]))
    
    trijet_mass_control = (control_good_boosted[:,0]+control_good_boosted[:,1]+control_good_boosted[:,2]).mass
    #calc inv mass of trijets by lorentz v. sum of three leading jets
    
    dijet1_mass_control = (control_good_boosted[:,0]+control_good_boosted[:,1]).mass
    #calc inv mass of first dijet combination

    dijet2_mass_control = (control_good_boosted[:,0]+control_good_boosted[:,2]).mass
    #calc inv mass of second dijet combination

    dijet3_mass_control = (control_good_boosted[:,1]+control_good_boosted[:,2]).mass
    #calc inv mass of third dijet combination
    
    mjjall_vs_mjjj_control = Hist(j3_bin, j2_bin)
    mjjall_vs_mjjj_control.fill(dijet_mass=dijet1_mass_control,trijet_mass=trijet_mass_control)
    mjjall_vs_mjjj_control.fill(dijet_mass=dijet2_mass_control,trijet_mass=trijet_mass_control)
    mjjall_vs_mjjj_control.fill(dijet_mass=dijet3_mass_control,trijet_mass=trijet_mass_control)
    
    trijet_mass_control_alternative = (control_alternative_good_boosted[:,0]+control_alternative_good_boosted[:,1]+control_alternative_good_boosted[:,2]).mass
    #calc inv mass of trijets by lorentz v. sum of three leading jets
    
    dijet1_mass_control_alternative = (control_alternative_good_boosted[:,0]+control_alternative_good_boosted[:,1]).mass
    #calc inv mass of first dijet combination

    dijet2_mass_control_alternative = (control_alternative_good_boosted[:,0]+control_alternative_good_boosted[:,2]).mass
    #calc inv mass of second dijet combination

    dijet3_mass_control_alternative = (control_alternative_good_boosted[:,1]+control_alternative_good_boosted[:,2]).mass
    
    mjjall_vs_mjjj_control_alternative = Hist(j3_bin, j2_bin)
    mjjall_vs_mjjj_control_alternative.fill(dijet_mass=dijet1_mass_control_alternative,trijet_mass=trijet_mass_control_alternative)
    mjjall_vs_mjjj_control_alternative.fill(dijet_mass=dijet2_mass_control_alternative,trijet_mass=trijet_mass_control_alternative)
    mjjall_vs_mjjj_control_alternative.fill(dijet_mass=dijet3_mass_control_alternative,trijet_mass=trijet_mass_control_alternative)
    
    j_mass_hist_x = hist.axis.Regular(label="Mass [GeV]", name="mass", bins=40, start=0, stop=1000)
    j1_mass_hist = Hist(j_mass_hist_x)
    j2_mass_hist = Hist(j_mass_hist_x)
    j3_mass_hist = Hist(j_mass_hist_x)
    j1_mass_hist.fill(mass=j1_mass)
    j2_mass_hist.fill(mass=j2_mass)
    j3_mass_hist.fill(mass=j3_mass)
    
    j1_mass_hist_control = Hist(j_mass_hist_x)
    j2_mass_hist_control = Hist(j_mass_hist_x)
    j3_mass_hist_control = Hist(j_mass_hist_x)
    j1_mass_hist_control.fill(mass=j1_mass_control)
    j2_mass_hist_control.fill(mass=j2_mass_control)
    j3_mass_hist_control.fill(mass=j3_mass_control)
    
    j1_mass_hist_control_alternative = Hist(j_mass_hist_x)
    j2_mass_hist_control_alternative = Hist(j_mass_hist_x)
    j3_mass_hist_control_alternative = Hist(j_mass_hist_x)
    j1_mass_hist_control_alternative.fill(mass=j1_mass_control_alternative)
    j2_mass_hist_control_alternative.fill(mass=j2_mass_control_alternative)
    j3_mass_hist_control_alternative.fill(mass=j3_mass_control_alternative)
    
    
    return events_total, j3_hist, j2_hist, mjj12_vs_mjjj, mjj13_vs_mjjj, mjj23_vs_mjjj, mjjall_vs_mjjj, mjjall_vs_mjjj_control, mjjall_vs_mjjj_control_alternative, j1_pNet, j2_pNet, j3_pNet, j1_mass_hist, j2_mass_hist, j3_mass_hist, j1_mass_hist_control, j2_mass_hist_control, j3_mass_hist_control, j1_mass_hist_control_alternative, j2_mass_hist_control_alternative, j3_mass_hist_control_alternative



#fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_2000_M2_1100_NANOAOD.root" #(on lxplus)
fname = "/STORE/ferencek/TRSM_XToHY_6b/2017/13TeV/NANOAOD/TRSM_XToHY_6b_M3_2000_M2_1100_NANOAOD.root" 

# MX = [400,800,1200,1600,2000,2400,2800,3200,3600,4000]
# MY = [260,300,700,1100,1500,1900,2300,2700,3100,3500,3900]

# for mx in MX:
#     for my in MY:
#         if my+130<mx:
#             fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_{0}_M2_{1}_NANOAOD.root".format(mx,my)
#             oFile   = "{0}_{1}".format(mx,my)
#             plotMassDist(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)

#         elif my+100==mx:
#             my = my-40
#             fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_{0}_M2_{1}_NANOAOD.root".format(mx,my)
#             oFile   = "{0}_{1}".format(mx,my)
#             plotMassDist(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)


def create_root_file(year="2017", sample="QCD2000", file="", file_path="", n_of_tagged_jets=2):
    events_total, j3_hist, j2_hist, mjj12_vs_mjjj, mjj13_vs_mjjj, mjj23_vs_mjjj, mjjall_vs_mjjj_signal, mjjall_vs_mjjj_control, mjjall_vs_mjjj_control_alternative, j1_pNet, j2_pNet, j3_pNet, j1_mass_hist, j2_mass_hist, j3_mass_hist, j1_mass_hist_control, j2_mass_hist_control, j3_mass_hist_control, j1_mass_hist_control_alternative, j2_mass_hist_control_alternative, j3_mass_hist_control_alternative = plotMassDist(fname, "2000-1100", processLabel="signal_2000-1100", eventsToRead=None, n_of_tagged_jets=n_of_tagged_jets)
    
    with uproot.recreate("XToHY_6b_2000_1100_{0}_b-tag.root".format(n_of_tagged_jets)) as fout:
        fout[f"events_total"] = events_total
        fout[f"j3_hist"] = j3_hist
        fout[f"j2_hist"] = j2_hist
        fout[f"mjj12_vs_mjjj"] = mjj12_vs_mjjj
        fout[f"mjj13_vs_mjjj"] = mjj13_vs_mjjj
        fout[f"mjj23_vs_mjjj"] = mjj23_vs_mjjj
        fout[f"mjjall_vs_mjjj_signal"] = mjjall_vs_mjjj_signal
        fout[f"mjjall_vs_mjjj_control"] = mjjall_vs_mjjj_control
        fout[f"mjjall_vs_mjjj_control_alternative"] = mjjall_vs_mjjj_control_alternative
        fout[f"j1_pNet"] = j1_pNet
        fout[f"j2_pNet"] = j2_pNet
        fout[f"j3_pNet"] = j3_pNet
        fout[f"j1_mass_signal"] = j1_mass_hist
        fout[f"j2_mass_signal"] = j2_mass_hist
        fout[f"j3_mass_signal"] = j3_mass_hist
        fout[f"j1_mass_control"] = j1_mass_hist_control
        fout[f"j2_mass_control"] = j2_mass_hist_control
        fout[f"j3_mass_control"] = j3_mass_hist_control      
        fout[f"j1_mass_control_alternative"] = j1_mass_hist_control_alternative
        fout[f"j2_mass_control_alternative"] = j2_mass_hist_control_alternative
        fout[f"j3_mass_control_alternative"] = j3_mass_hist_control_alternative
        
if __name__ == '__main__':
    for i in range(3):
        create_root_file(n_of_tagged_jets=i)