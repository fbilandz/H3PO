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
import ROOT 

def normalize_hist(h):
    integral = np.sum(np.sum(h.to_numpy()[0]))
    h_res = Hist(h.axes[0])
    h_res.name = h.name
    h_res.label = h.label
    for i in range(len(h.to_numpy()[0])):
        h_res[i] = h.to_numpy()[0][i]/ integral

    return h_res

def plot_templates():
    # 0 b-tag
    for i in range(3):
        with uproot.open("FittingArea/QCD17_{0}_b-tag.root".format(i)) as file:
            qcd_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
            qcd_signal.name = "QCD"
            qcd_signal_x = normalize_hist(qcd_signal.project('xaxis'))
            qcd_signal_y = normalize_hist(qcd_signal.project('yaxis'))
            
        with uproot.open("FittingArea/TTbar17_{0}_b-tag.root".format(i)) as file:
            ttbar_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
            ttbar_signal.name = "ttbar"
            ttbar_signal_x = normalize_hist(ttbar_signal.project('xaxis'))
            ttbar_signal_y = normalize_hist(ttbar_signal.project('yaxis'))
            plt.style.use([hep.style.CMS])
            plt.tight_layout()
            hep.histplot(qcd_signal_x, yerr=False, histtype="step")
            hep.histplot(ttbar_signal_x, yerr=False, histtype="step")
            
            plt.ylabel("N/a.u.",horizontalalignment='right', y=1.0)
            plt.xlabel("Trijet Mass [GeV]")
            plt.legend()
            plt.savefig("compare_shape_{0}_x.png".format(i))
            plt.cla()
            plt.clf()
            
            plt.style.use([hep.style.CMS])
            plt.tight_layout()
            hep.histplot(qcd_signal_y, yerr=False, histtype="step")
            hep.histplot(ttbar_signal_y, yerr=False, histtype="step")
            
            plt.ylabel("N/a.u.",horizontalalignment='right', y=1.0)
            plt.xlabel("Trijet Mass [GeV]")
            plt.legend()
            plt.savefig("compare_shape_{0}_y.png".format(i))
            plt.cla()
            plt.clf()
        # qcd_file = ROOT.TFile.Open("FittingArea/QCD17_{0}_b-tag.root".format(i))
        # qcd_signal = qcd_file.Get("mjjall_vs_mjjj_signal_rebinned")
        # qcd_signal.Plot()
        
if __name__ == '__main__':
    plot_templates()    
    