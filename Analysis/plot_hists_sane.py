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

def scale_to_bin_width(hist):
    h_res = Hist(hist.axes[0])
    h_res.name = hist.name
    h_res.label = hist.label
    error_data = []
    for i in range(len(hist.to_numpy()[0])):
        width = hist.to_numpy()[1][i + 1] - hist.to_numpy()[1][i]
        h_res[i] = hist.to_numpy()[0][i]/ width
        error = np.sqrt(hist.to_numpy()[0][i])/width
        error_data.append(error)
    return h_res, error_data

def hist_yield(hist):
    return np.sum(np.sum(hist.to_numpy()[0]))/3

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
    with uproot.open("FittingArea/QCD17_sane.root") as file:
        qcd_signal = file["j3_hist"].to_hist()
        qcd_signal.name = "QCD"
        print("QCD yield: ", hist_yield(qcd_signal))
        # qcd_signal.project("trijet_mass").plot()
        lumi_text = "$41.5 fb^{-1} (13 TeV)$"
        cms_text = "Work in progress"
        plot_hist(qcd_signal, lumi_text, 
                cms_text, "Trijet Mass [GeV]", 
                "Dijet Mass [GeV]", "j3_mass_qcd_signal_sane.png")
        # j3_hist_unfolded = file["unwrapped_mjjall_vs_mjjj"].to_hist()
        # plot_hist(j3_hist_unfolded, lumi_text, 
        #         cms_text, "Event count", 
        #         "Bin number", "j3_mass_qcd_unfolded.png")
        
        
    with uproot.open('background/scaled/JetHT17_sane.root') as file:
        data_hist_signal = file["j3_hist"].to_hist()
        data_hist_signal.name = "Data"
        
    with uproot.open('FittingArea/TTbar17_sane.root') as file:
        ttbar_signal = file["j3_hist"].to_hist()
        ttbar_signal.name = "TTbar"

        print("ttbar yield: ", hist_yield(ttbar_signal))
        plot_hist(ttbar_signal, lumi_text, 
                cms_text, "Trijet Mass [GeV]", 
                "Dijet Mass [GeV]", "j3_mass_ttbar_sane.png")
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        
        hep.histplot(qcd_signal, stack=True, histtype="fill", label="QCD")
        hep.histplot(ttbar_signal, stack=True, histtype="fill", label="TTbar")
        #background_plot_x.plot(stack=True, histtype="fill")
        #data_0_btag_x.plot(histtype="errorbar", label="Data", color="black")
        hep.histplot(data_hist_signal, yerr=True, histtype="errorbar", label="Data", color="black")
        
        hep.cms.text("Work in progress",loc=0)   
        hep.cms.lumitext(lumi_text)
        plt.ylabel("Event count",horizontalalignment='right', y=1.0)
        plt.xlabel("Trijet Mass [GeV]")
        plt.legend()
        plt.savefig("j3_mass_sane.png")
        plt.cla()
        plt.clf()
        
        # plt.style.use([hep.style.CMS])
        # plt.tight_layout()
        # qcd_0_btag_y, qcd_0_btag_ey = scale_to_bin_width(qcd_signal.project("yaxis"))
        # ttbar_0_btag_y, qcd_0_btag_ey = scale_to_bin_width(ttbar_signal.project("yaxis"))
        # data_0_btag_y, data_0_btag_ey = scale_to_bin_width(data_hist_signal.project("yaxis"))
        
        # hep.histplot(qcd_0_btag_y, stack=True, histtype="fill", label="QCD")
        # hep.histplot(ttbar_0_btag_y, stack=True, histtype="fill", label="TTbar")
        # #background_plot_y.plot(stack=True, histtype="fill")
        # # data_0_btag_y.plot(histtype="errorbar", label="Data", color="black")
        # hep.histplot(data_0_btag_y, yerr=data_0_btag_ey, histtype="errorbar", label="Data", color="black")
        
        # hep.cms.text("Work in progress",loc=0)
        # lumiText = "$41.5 fb^{-1} (13 TeV)$"    
        # hep.cms.lumitext(lumiText)
        # plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
        # plt.xlabel("Dijet Mass [GeV]")
        # plt.legend()
        # plt.savefig("j2_sane.png")
        # plt.cla()
        # plt.clf()
        
        
    # 1-btag
    # with uproot.open("FittingArea/QCD17_1_b-tag.root") as file:
    #     j3_hist_qcd = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #     j3_hist_qcd.name = "QCD"
    #     # j3_hist_qcd.project("trijet_mass").plot()
    #     print("QCD yield: ", hist_yield(j3_hist_qcd))
    #     ax = j3_hist_qcd.project("xaxis").axes[0]
    #     cat = hist.axis.StrCategory(["QCD", "TTbar", "Signal"], name="cat")
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     j3_hist_qcd.plot()
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
    #     plt.xlabel("Trijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("j3_mass_qcd_1_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    # with uproot.open('FittingArea/XToHY_6b_2000_1100_1_b-tag.root') as file:
    #     signal_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #     j3_hist_signal.name = "Signal"
    #     print("signal yield: ", hist_yield(j3_hist_signal))
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     j3_hist_signal.plot()
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
    #     plt.xlabel("Trijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjj_vs_mjjj_signal_signal_1_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    # with uproot.open('background/scaled/JetHT17_1_b-tag.root') as file:
    #     data_hist_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #     data_hist_signal.name = "Data"
        
    # with uproot.open('FittingArea/TTbar17_1_b-tag.root') as file:
    #     ttbar_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #     j3_hist_ttbar.name = "TTbar"
    #     print("ttbar yield: ", hist_yield(j3_hist_ttbar))
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     j3_hist_ttbar.plot()
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
    #     plt.xlabel("Trijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjj_vs_mjjj_ttbar_1_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     qcd_1_btag_x = scale_to_bin_width(j3_hist_qcd.project("xaxis"))
    #     ttbar_1_btag_x = scale_to_bin_width(j3_hist_ttbar.project("xaxis"))
    #     signal_1_btag_x = scale_to_bin_width(j3_hist_signal.project("xaxis"))
    #     data_1_btag_x = scale_to_bin_width(data_hist_signal.project("xaxis"))
        
    #     background_plot_x = Stack(qcd_1_btag_x, ttbar_1_btag_x)
    #     background_plot_x.plot(stack=True, histtype="fill")
    #     (0.1 * signal_1_btag_x).plot(label="Signal")
    #     data_1_btag_x.plot(label="Data", histtype="errorbar")
        
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #     plt.xlabel("Trijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjjj_signal_1_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     qcd_1_btag_y = scale_to_bin_width(j3_hist_qcd.project("yaxis"))
    #     ttbar_1_btag_y = scale_to_bin_width(j3_hist_ttbar.project("yaxis"))
    #     signal_1_btag_y = scale_to_bin_width(j3_hist_signal.project("yaxis"))
        
    #     background_plot_y = Stack(qcd_1_btag_y, ttbar_1_btag_y)
    #     background_plot_y.plot(stack=True, histtype="fill")
    #     signal_1_btag_y.plot(label="Signal")
        
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #     plt.xlabel("Dijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjj_signal_1_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    # # 2 b-tag
    # with uproot.open("FittingArea/QCD17_2_b-tag.root") as file:
    #     j3_hist_qcd = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #     j3_hist_qcd.name = "QCD"
    #     # j3_hist_qcd.project("trijet_mass").plot()
    #     ax = j3_hist_qcd.project("xaxis").axes[0]
    #     cat = hist.axis.StrCategory(["QCD", "TTbar", "Signal"], name="cat")
    #     print("qcd yield: ", hist_yield(j3_hist_qcd))
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     j3_hist_qcd.plot()
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
    #     plt.xlabel("Trijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjj_vs_mjjj_qcd_2_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    # with uproot.open('FittingArea/XToHY_6b_2000_1100_2_b-tag.root') as file:
    #     j3_hist_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #     j3_hist_signal.name = "Signal"
    #     print("signal yield: ", hist_yield(j3_hist_signal))
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     j3_hist_signal.plot()
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
    #     plt.xlabel("Trijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjj_vs_mjjj_signal_2_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    # with uproot.open('background/scaled/JetHT17_2_b-tag.root') as file:
    #     data_hist_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #     data_hist_signal.name = "Data"
        
    # with uproot.open('FittingArea/TTbar17_2_b-tag.root') as file:
    #     j3_hist_ttbar = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #     j3_hist_ttbar.name = "TTbar"
    #     print("ttbar yield: ", hist_yield(j3_hist_ttbar))
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     j3_hist_ttbar.plot()
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel("Dijet Mass [GeV]", horizontalalignment='right', y=1.0)
    #     plt.xlabel("Trijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjj_vs_mjjj_ttbar_2_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     qcd_2_btag_x = scale_to_bin_width(j3_hist_qcd.project("xaxis"))
    #     ttbar_2_btag_x = scale_to_bin_width(j3_hist_ttbar.project("xaxis"))
    #     signal_2_btag_x = scale_to_bin_width(j3_hist_signal.project("xaxis"))
    #     data_2_btag_x = scale_to_bin_width(data_hist_signal.project("xaxis"))
        
    #     background_plot_x = Stack(qcd_2_btag_x, ttbar_2_btag_x)
    #     background_plot_x.plot(stack=True, histtype="fill")
    #     (0.1 * signal_2_btag_x).plot(label="Signal")
    #     data_2_btag_x.plot(label="Data", histtype="errorbar")
        
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #     plt.xlabel("Trijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjjj_signal_2_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
    #     plt.style.use([hep.style.CMS])
    #     plt.tight_layout()
    #     qcd_2_btag_y = scale_to_bin_width(j3_hist_qcd.project("yaxis"))
    #     ttbar_2_btag_y = scale_to_bin_width(j3_hist_ttbar.project("yaxis"))
    #     signal_2_btag_y = scale_to_bin_width(j3_hist_signal.project("yaxis"))
        
    #     background_plot_y = Stack(qcd_2_btag_y, ttbar_2_btag_y)
    #     background_plot_y.plot(stack=True, histtype="fill")
    #     signal_2_btag_y.plot(label="Signal")
        
    #     hep.cms.text("Work in progress",loc=0)
    #     lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #     hep.cms.lumitext(lumiText)
    #     plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #     plt.xlabel("Dijet Mass [GeV]")
    #     plt.legend()
    #     plt.savefig("mjj_signal_2_b-tag.png")
    #     plt.cla()
    #     plt.clf()
        
if __name__ == '__main__':
    plot_hists()