#!/usr/bin/env python
# -*- coding: utf-8 -*

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


def plotMassDist(fname,oFile,processLabel="signal",eventsToRead=None, n_of_tagged_jet=0):
    n_of_tagged_jet = int(n_of_tagged_jet)
    good_boosted, control_good_boosted, control_alternative_good_boosted, total_events, j2_cutless_mass = data_boosted(fname,oFile,processLabel="JetHT_BACKGROUND",eventsToRead=None, n_of_tagged_jets=n_of_tagged_jet)

    trijet_mass_signal = (good_boosted[:,0]+good_boosted[:,1]+good_boosted[:,2]).mass
    j1_mass = good_boosted[:,0].msoftdrop
    j2_mass = good_boosted[:,1].msoftdrop
    j3_mass = good_boosted[:,2].msoftdrop
    
    j1_mass_control = control_good_boosted[:,0].msoftdrop
    j2_mass_control = control_good_boosted[:,1].msoftdrop
    j3_mass_control = control_good_boosted[:,2].msoftdrop
    
    j1_mass_control_alternative = control_alternative_good_boosted[:,0].msoftdrop
    j2_mass_control_alternative = control_alternative_good_boosted[:,1].msoftdrop
    j3_mass_control_alternative = control_alternative_good_boosted[:,2].msoftdrop
    #calc inv mass of trijets by lorentz v. sum of three leading jets

    j3_bin = hist.axis.Regular(label="Trijet Mass [GeV]", name="trijet_mass", bins=60, start=0, stop=6000)
    # j3_cat = hist.axis.StrCategory(label='Trijets', name='trijet', categories=[processLabel])

    j3_hist = Hist(j3_bin)
    j3_hist.fill(trijet_mass=trijet_mass_signal)

    events_cat  = hist.axis.Integer(0, 8, underflow=False, overflow=False)
    events_total = Hist(events_cat)
    for i in range(len(total_events)):
        events_total[i] = total_events[i]
    # plt.style.use([hep.style.CMS])
    # j3_hist.plot(color="black")
    # hep.cms.text("Work in progress",loc=0)
    # plt.ylabel("Event count",horizontalalignment='right', y=1.0)
    # plt.legend()
    # plt.savefig("MJJJ_btag_{0}.png".format(oFile))
    # plt.cla()
    # plt.clf()

    #-----MJJ calc and plotting-----#


    dijet1_mass_signal = (good_boosted[:,0]+good_boosted[:,1]).mass
    #calc inv mass of first dijet combination

    dijet2_mass_signal = (good_boosted[:,0]+good_boosted[:,2]).mass
    #calc inv mass of second dijet combination

    dijet3_mass_signal = (good_boosted[:,1]+good_boosted[:,2]).mass
    #calc inv mass of third dijet combination


    j2_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=40, start=0, stop=4000)
    j2_cat = hist.axis.StrCategory(label='Dijets', name='dijet', categories=["12 Pair","13 Pair","23 Pair"])

    j2_hist = Hist(j2_bin, j2_cat)

    j2_hist.fill(dijet="12 Pair", dijet_mass=dijet1_mass_signal)
    j2_hist.fill(dijet="13 Pair", dijet_mass=dijet2_mass_signal)
    j2_hist.fill(dijet="23 Pair", dijet_mass=dijet3_mass_signal)

    mjj12_vs_mjjj = Hist(j3_bin,j2_bin)
    mjj12_vs_mjjj.fill(dijet_mass=dijet1_mass_signal,trijet_mass=trijet_mass_signal)
    mjj13_vs_mjjj = Hist(j3_bin,j2_bin)
    mjj13_vs_mjjj.fill(dijet_mass=dijet2_mass_signal,trijet_mass=trijet_mass_signal)
    mjj23_vs_mjjj = Hist(j3_bin,j2_bin)
    mjj23_vs_mjjj.fill(dijet_mass=dijet3_mass_signal,trijet_mass=trijet_mass_signal)
    
    mjjall_vs_mjjj_signal = Hist(j3_bin, j2_bin)
    mjjall_vs_mjjj_signal.fill(dijet_mass=dijet1_mass_signal,trijet_mass=trijet_mass_signal)
    mjjall_vs_mjjj_signal.fill(dijet_mass=dijet2_mass_signal,trijet_mass=trijet_mass_signal)
    mjjall_vs_mjjj_signal.fill(dijet_mass=dijet3_mass_signal,trijet_mass=trijet_mass_signal)
    
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
    
    j_mass_hist_x = hist.axis.Regular(label="Mass [GeV]", name="mass", bins=40, start=0, stop=1000)
    j1_mass_hist = Hist(j_mass_hist_x)
    j2_mass_hist = Hist(j_mass_hist_x)
    j3_mass_hist = Hist(j_mass_hist_x)
    j1_mass_hist.fill(mass=j1_mass)
    j2_mass_hist.fill(mass=j2_mass)
    j3_mass_hist.fill(mass=j3_mass)
    
    j2_mass_cutless_hist = Hist(j_mass_hist_x)
    j2_mass_cutless_hist.fill(mass=j2_cutless_mass)
    
    j1_mass_hist_control = Hist(j_mass_hist_x)
    j2_mass_hist_control = Hist(j_mass_hist_x)
    j3_mass_hist_control = Hist(j_mass_hist_x)
    j1_mass_hist_control.fill(mass=j1_mass_control)
    j2_mass_hist_control.fill(mass=j2_mass_control)
    j3_mass_hist_control.fill(mass=j3_mass_control)
    
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
    
    j1_mass_hist_control_alternative = Hist(j_mass_hist_x)
    j2_mass_hist_control_alternative = Hist(j_mass_hist_x)
    j3_mass_hist_control_alternative = Hist(j_mass_hist_x)
    j1_mass_hist_control_alternative.fill(mass=j1_mass_control_alternative)
    j2_mass_hist_control_alternative.fill(mass=j2_mass_control_alternative)
    j3_mass_hist_control_alternative.fill(mass=j3_mass_control_alternative)
    
    return events_total, j3_hist, j2_hist, mjj12_vs_mjjj, mjj13_vs_mjjj, mjj23_vs_mjjj, mjjall_vs_mjjj_signal, mjjall_vs_mjjj_control, mjjall_vs_mjjj_control_alternative, j1_pNet, j2_pNet, j3_pNet, j1_mass_hist, j2_mass_hist, j3_mass_hist, j1_mass_hist_control, j2_mass_hist_control, j3_mass_hist_control, j1_mass_hist_control_alternative, j2_mass_hist_control_alternative, j3_mass_hist_control_alternative, j2_mass_cutless_hist

#fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_2000_M2_1100_NANOAOD.root" #(on lxplus)
 

from os import listdir
from os.path import isfile, join

def create_root_files(year="2017", sample="QCD2000", file="", file_path="", n_of_tagged_jets=0):
    total_events, j3_hist, j2_hist, mjj12_vs_mjjj, mjj13_vs_mjjj, mjj23_vs_mjjj, mjjall_vs_mjjj_signal, mjjall_vs_mjjj_control, mjjall_vs_mjjj_control_alternative, j1_pNet, j2_pNet, j3_pNet, j1_mass_hist, j2_mass_hist, j3_mass_hist, j1_mass_hist_control, j2_mass_hist_control, j3_mass_hist_control, j1_mass_hist_control_alternative, j2_mass_hist_control_alternative, j3_mass_hist_control_alternative, j2_mass_cutless_hist = plotMassDist(file_path, "{0}-{1}".format(sample, file), processLabel=sample, eventsToRead=None, n_of_tagged_jet=n_of_tagged_jets)
    
    with uproot.recreate("{0}-{1}.root".format(sample, file)) as fout:
        fout[f"total_events"] = total_events
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
        fout[f" j2_mass_cutless_hist"] = j2_mass_cutless_hist
        
if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Do -h to see usage")

    parser.add_argument('-c', '--config', help='Job config file in JSON format')
    parser.add_argument('-y', '--year', help='Dataset year',default="2017")
    parser.add_argument('-s', '--sample', help='Sample name', default="QCD2000")
    parser.add_argument('-f', '--file', help='File name')
    parser.add_argument('-fp', '--file_path', help='File path')
    parser.add_argument('-nt', '--n_of_tagged_jets', help='Number of b-tagged jets', default=0)
    args = parser.parse_args()
    create_root_files(year=args.year, sample=args.sample, file=args.file, file_path=args.file_path, n_of_tagged_jets=args.n_of_tagged_jets)