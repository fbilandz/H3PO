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
    
    with uproot.open("/users/fbilandzija/CMSSW_10_6_14/src/2DAlphabet/Run2_hhh_loose_ttbar/1_area/plots_fit_b/all_plots.root") as file:
        qcd_fail = file["qcd_fail_postfit_2D"].to_hist()
        qcd_fail.name = "QCD"
        qcd_pass = file["qcd_1_pass_postfit_2D"].to_hist()

        
        h_res = Hist(qcd_fail.axes[0], qcd_fail.axes[1])
        h_res.name = qcd_fail.name
        h_res.label = qcd_fail.label
        print(qcd_fail.to_numpy()[0])
        for i in range(len(qcd_fail.to_numpy()[0])):
            for j in range(len(qcd_fail.to_numpy()[0][i])):
                if qcd_pass.to_numpy()[0][i][j] == 0:
                    h_res[i, j] = 0
                else:
                    h_res[i, j] = qcd_pass.to_numpy()[0][i][j] / qcd_fail.to_numpy()[0][i][j]
                    
        
        # for i in range(len(hist.to_numpy()[0])):
        #     width = hist.to_numpy()[1][i + 1] - hist.to_numpy()[1][i]
        #     h_res[i] = hist.to_numpy()[0][i]/ width

            

        # qcd_signal.project("trijet_mass").plot()
        
        # j3_hist_unfolded = file["unwrapped_mjjall_vs_mjjj"].to_hist()
        # plot_hist(j3_hist_unfolded, lumi_text, 
        #         cms_text, "Event count", 
        #         "Bin number", "mjj_vs_mjjj_qcd_unfolded.png")
        
    
        
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        
        # hep.histplot(qcd_control[2:20], stack=True, histtype="fill", label="QCD")
        # hep.histplot(ttbar_control[2:20], stack=True, histtype="fill", label="TTbar")
        # #background_plot_y.plot(stack=True, histtype="fill")
        # # hep.histplot(0.1 * signal_control, stack=False, label="Signal")
        # #data_hist_control.plot(histtype="errorbar", label="Data", color="black")
        # hep.histplot(data_hist_control[2:20], histtype="errorbar", label="Data", color="black")
        
        hep.hist2dplot(h_res, cmin=0.00001)
        
        hep.cms.text("Work in progress",loc=0)
        lumiText = "$138 fb^{-1} (13 TeV)$"    
        hep.cms.lumitext(lumiText)
        plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
        plt.xlabel("Trijet Mass [GeV]")
        plt.legend()
        plt.savefig("rpf_plot_ttbar_run2.png".format(i))
        plt.cla()
        plt.clf()
            
if __name__ == '__main__':
    plot_hists()