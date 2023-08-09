import uproot
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist, Stack
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import coffea.processor as processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema, schemas
import numpy as np
import mplhep as hep
from Selection import *
from os import listdir, getcwd, system
from os.path import isfile, join

def plot_hist(hist_to_plot, lumi_text, cms_text, xlabel, ylabel, fig_name):
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hist_to_plot.plot()
    hep.cms.text(cms_text, loc=0)
    # lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    hep.cms.lumitext(lumi_text)
    plt.ylabel(ylabel, horizontalalignment='right', y=1.0)
    plt.xlabel(xlabel)
    plt.legend()
    #plt.savefig("mjj_vs_mjjj_qcd_0_b-tag.png")
    plt.savefig(fig_name)
    plt.cla()
    plt.clf()

def plot_hists():
    # 0 b-tag
    for i in range(1):
        with uproot.open("FittingArea/QCD17_{0}_b-tag.root".format(i)) as file:
            qcd_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
            qcd_signal.name = "QCD"
            qcd_control = file[" j2_mass_cutless_hist"].to_hist()
            qcd_control.name = "QCD"
            qcd_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
            qcd_control_alternative.name = "QCD"
            # qcd_signal.project("trijet_mass").plot()
            
            # j3_hist_unfolded = file["unwrapped_mjjall_vs_mjjj"].to_hist()
            # plot_hist(j3_hist_unfolded, lumi_text, 
            #         cms_text, "Event count", 
            #         "Bin number", "mjj_vs_mjjj_qcd_unfolded.png")
            
        with uproot.open('FittingArea/XToHY_6b_2000_1100_{0}_b-tag.root'.format(i)) as file:
            signal_control = file["j2_mass_control"].to_hist()
            signal_control.name = "Signal"
            
            
        with uproot.open('FittingArea/JetHT17_fail.root'.format(i)) as file:
            data_hist_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
            data_hist_signal.name = "Data"
            data_hist_control = file[" j2_mass_cutless_hist"].to_hist()
            data_hist_control.name = "Data"
            data_hist_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
            data_hist_control_alternative.name = "Data"
            
            plt.style.use([hep.style.CMS])
            plt.tight_layout()
            
            hep.hist2dplot(data_hist_signal, label="Data", cmin = 1)
            
            hep.cms.text("Work in progress",loc=0)
            lumiText = "$41.5 fb^{-1} (13 TeV)$"    
            hep.cms.lumitext(lumiText)
            plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
            plt.xlabel("Trijet Mass [GeV]")
            plt.legend()
            plt.savefig("data_fail_SR.png".format(i))
            plt.cla()
            plt.clf()
            
            
        with uproot.open('FittingArea/TTbar17_{0}_b-tag.root'.format(i)) as file:
            ttbar_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
            ttbar_signal.name = "TTbar"
            ttbar_control = file[" j2_mass_cutless_hist"].to_hist()
            ttbar_control.name = "TTbar"
            ttbar_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
            ttbar_control_alternative.name = "TTbar"
            
            plt.style.use([hep.style.CMS])
            plt.tight_layout()
            
            hep.histplot(qcd_control[2:20], stack=True, histtype="fill", label="QCD")
            hep.histplot(ttbar_control[2:20], stack=True, histtype="fill", label="TTbar")
            #background_plot_y.plot(stack=True, histtype="fill")
            # hep.histplot(0.1 * signal_control, stack=False, label="Signal")
            #data_hist_control.plot(histtype="errorbar", label="Data", color="black")
            hep.histplot(data_hist_control[2:20], histtype="errorbar", label="Data", color="black")
            
            hep.cms.text("Work in progress",loc=0)
            lumiText = "$41.5 fb^{-1} (13 TeV)$"    
            hep.cms.lumitext(lumiText)
            plt.ylabel("Event count", horizontalalignment='right', y=1.0)
            plt.xlabel("Jet Mass [GeV]")
            plt.legend()
            plt.savefig("j2_mass_control_no_b-tag.png".format(i))
            plt.cla()
            plt.clf()
            
if __name__ == '__main__':
    plot_hists()