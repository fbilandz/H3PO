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
# 0 b-ta
        
    with uproot.open('FittingArea/JetHT17_fail.root') as file:
        data_hist_signal = file["mjjall_vs_mjjj_signal_rebinned_bkg_estimated_pass"].to_hist()
        data_hist_signal.name = "Data"
        
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        
        hep.hist2dplot(data_hist_signal, label="Data", cmin = 0.001)
        
        hep.cms.text("Work in progress",loc=0)
        lumiText = "$41.5 fb^{-1} (13 TeV)$"    
        hep.cms.lumitext(lumiText)
        plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
        plt.xlabel("Trijet Mass [GeV]")
        plt.legend()
        plt.savefig("data_SR_estimated_bkg.png")
        plt.cla()
        plt.clf()
        
            
if __name__ == '__main__':
    plot_hists()