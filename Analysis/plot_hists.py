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
    # 0 b-tag
    with uproot.open("FittingArea/QCD_Run2_pass.root") as file:
        qcd_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        qcd_signal.name = "QCD"
        # qcd_control = file["mjjall_vs_mjjj_control_rebinned"].to_hist()
        # qcd_control.name = "QCD"
        qcd_control_integral_hist = file["mjjall_vs_mjjj_control"].to_hist()
        print("QCD Control Integral yield: ", hist_yield(qcd_control_integral_hist))
        qcd_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        qcd_control_alternative.name = "QCD"
        print("QCD yield: ", hist_yield(qcd_signal))
        # qcd_signal.project("trijet_mass").plot()
        ax = qcd_signal.project("xaxis").axes[0]
        cat = hist.axis.StrCategory(["QCD", "TTbar", "Signal"], name="cat")
        lumi_text = "$138 fb^{-1} (13 TeV)$"
        cms_text = "Work in progress"
        plot_hist(qcd_signal, lumi_text, 
                cms_text, "Trijet Mass [GeV]", 
                "Dijet Mass [GeV]", "mjj_vs_mjjj_qcd_signal_pass_run2.png")
        
        # print("QCD control yield: ", hist_yield(qcd_control))
        # plot_hist(qcd_control, lumi_text, 
        #         cms_text, "Trijet Mass [GeV]", 
        #         "Dijet Mass [GeV]", "mjj_vs_mjjj_qcd_control_{0}_b-tag.png".format(i))
        
        print("QCD control alternative yield: ", hist_yield(qcd_control_alternative))
        plot_hist(qcd_control_alternative, lumi_text, 
                cms_text, "Trijet Mass [GeV]", 
                "Dijet Mass [GeV]", "mjj_vs_mjjj_qcd_control_alt_pass_run2.png")
        # j3_hist_unfolded = file["unwrapped_mjjall_vs_mjjj"].to_hist()
        # plot_hist(j3_hist_unfolded, lumi_text, 
        #         cms_text, "Event count", 
        #         "Bin number", "mjj_vs_mjjj_qcd_unfolded.png")
        
    with uproot.open('FittingArea/XToHY_6b_2000_1100_pass_Run2.root') as file:
        signal_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        signal_signal.name = "Signal"
        # signal_control = file["mjjall_vs_mjjj_control_rebinned"].to_hist()
        # signal_control.name = "Signal"
        signal_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        signal_control_alternative.name = "Signal"
        print("signal yield: ", hist_yield(signal_signal))
        plot_hist(signal_signal, lumi_text, 
                cms_text, "Trijet Mass [GeV]", 
                "Dijet Mass [GeV]", "mjj_vs_mjjj_signal_signal_pass_run2.png")
        # print("signal control yield: ", hist_yield(signal_control))
        # plot_hist(signal_control, lumi_text, 
        #         cms_text, "Trijet Mass [GeV]", 
        #         "Dijet Mass [GeV]", "mjj_vs_mjjj_signal_control_pass.png")
        print("signal control alt yield: ", hist_yield(signal_control_alternative))
        plot_hist(signal_control_alternative, lumi_text, 
                cms_text, "Trijet Mass [GeV]", 
                "Dijet Mass [GeV]", "mjj_vs_mjjj_signal_control_alt_pass_run2.png")
        
    with uproot.open('FittingArea/JetHT_Run2_pass.root') as file:
        data_hist_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        data_hist_signal.name = "Data"
        data_hist_control = file["mjjall_vs_mjjj_control_rebinned"].to_hist()
        data_hist_control.name = "Data"
        data_hist_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        data_hist_control_alternative.name = "Data"
        print("data control yield: ", hist_yield(data_hist_control))
        
    with uproot.open('FittingArea/TTbar_Run2_pass.root') as file:
        ttbar_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        ttbar_signal.name = "TTbar"
        # ttbar_control = file["mjjall_vs_mjjj_control_rebinned"].to_hist()
        ttbar_control_integral_hist = file["mjjall_vs_mjjj_control"].to_hist()
        # print("TTbar Integral yield: ", hist_yield(ttbar_control_integral_hist))
        # ttbar_control.name = "TTbar"
        ttbar_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        ttbar_control_alternative.name = "TTbar"
        print("ttbar yield: ", hist_yield(ttbar_signal))
        plot_hist(ttbar_signal, lumi_text, 
                cms_text, "Trijet Mass [GeV]", 
                "Dijet Mass [GeV]", "mjj_vs_mjjj_ttbar_signal_pass.png")
        # print("ttbar control yield: ", hist_yield(ttbar_control))
        # plot_hist(ttbar_control, lumi_text, 
        #         cms_text, "Trijet Mass [GeV]", 
        #         "Dijet Mass [GeV]", "mjj_vs_mjjj_ttbar_control_0_b-tag.png")
        
        print("ttbar control alt yield: ", hist_yield(ttbar_control_alternative))
        plot_hist(ttbar_control_alternative, lumi_text, 
                cms_text, "Trijet Mass [GeV]", 
                "Dijet Mass [GeV]", "mjj_vs_mjjj_ttbar_alt_control_pass.png")
        
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        qcd_0_btag_x, qcd_0_btag_ex = scale_to_bin_width(qcd_signal.project("xaxis"))
        ttbar_0_btag_x, ttbar_0_btag_ex = scale_to_bin_width(ttbar_signal.project("xaxis"))
        signal_0_btag_x, signal_0_btag_ex = scale_to_bin_width(signal_signal.project("xaxis"))
        data_0_btag_x, data_0_btag_ex = scale_to_bin_width(data_hist_signal.project("xaxis"))
        
        hep.histplot(qcd_0_btag_x, stack=True, histtype="fill", label="QCD")
        hep.histplot(ttbar_0_btag_x, stack=True, histtype="fill", label="TTbar")
        #background_plot_x.plot(stack=True, histtype="fill")
        hep.histplot(1* signal_0_btag_x, stack=False, label="Signal")
        #data_0_btag_x.plot(histtype="errorbar", label="Data", color="black")
        # hep.histplot(data_0_btag_x, yerr=data_0_btag_ex, histtype="errorbar", label="Data", color="black")
        
        hep.cms.text("Work in progress",loc=0)   
        hep.cms.lumitext(lumi_text)
        plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
        plt.xlabel("Trijet Mass [GeV]")
        plt.legend()
        plt.savefig("mjjj_signal_pass_run2.png")
        plt.cla()
        plt.clf()
        
        
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        qcd_0_btag_y, qcd_0_btag_ey = scale_to_bin_width(qcd_signal.project("yaxis"))
        ttbar_0_btag_y, qcd_0_btag_ey = scale_to_bin_width(ttbar_signal.project("yaxis"))
        signal_0_btag_y, qcd_0_btag_ey = scale_to_bin_width(signal_signal.project("yaxis"))
        data_0_btag_y, data_0_btag_ey = scale_to_bin_width(data_hist_signal.project("yaxis"))
        
        hep.histplot(qcd_0_btag_y, stack=True, histtype="fill", label="QCD")
        hep.histplot(ttbar_0_btag_y, stack=True, histtype="fill", label="TTbar")
        #background_plot_y.plot(stack=True, histtype="fill")
        hep.histplot(1 *signal_0_btag_y, stack=False, label="Signal")
        #data_0_btag_y.plot(histtype="errorbar", label="Data", color="black")
        #hep.histplot(data_0_btag_y, yerr=data_0_btag_ey, histtype="errorbar", label="Data", color="black")
        
        hep.cms.text("Work in progress",loc=0)
        lumiText = "$138 fb^{-1} (13 TeV)$"    
        hep.cms.lumitext(lumiText)
        plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
        plt.xlabel("Dijet Mass [GeV]")
        plt.legend()
        plt.savefig("mjj_signal_pass_run2.png")
        plt.cla()
        plt.clf()
        
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        qcd_btag_x, qcd_btag_ex = scale_to_bin_width(qcd_control_alternative.project("xaxis"))
        ttbar_btag_x, ttbar_btag_ex = scale_to_bin_width(ttbar_control_alternative.project("xaxis"))
        signal_btag_x, signal_btag_ex = scale_to_bin_width(signal_control_alternative.project("xaxis"))
        data_btag_x, data_btag_ex = scale_to_bin_width(data_hist_control_alternative.project("xaxis"))
        
        hep.histplot(qcd_btag_x, stack=True, histtype="fill", label="QCD")
        hep.histplot(ttbar_btag_x, stack=True, histtype="fill", label="TTbar")
        #background_plot_x.plot(stack=True, histtype="fill")
        hep.histplot(1 * signal_btag_x, stack=False, label="Signal")
        #data_btag_x.plot(histtype="errorbar", label="Data", color="black")
        hep.histplot(data_btag_x, yerr=data_btag_ex, histtype="errorbar", label="Data", color="black")
        
        hep.cms.text("Work in progress",loc=0)   
        hep.cms.lumitext(lumi_text)
        plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
        plt.xlabel("Trijet Mass [GeV]")
        plt.legend()
        plt.savefig("mjjj_control_alternative_pass_run2.png")
        plt.cla()
        plt.clf()
        
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        hep.histplot(data_btag_x / (qcd_btag_x + ttbar_btag_x),  label="Ratio")
        
        hep.cms.text("Work in progress",loc=0)   
        hep.cms.lumitext(lumi_text)
        plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
        plt.xlabel("Trijet Mass [GeV]")
        plt.legend()
        plt.savefig("mjjj_ratio_pass_run2.png")
        plt.cla()
        plt.clf()
        
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        qcd_btag_y, qcd_btag_ey = scale_to_bin_width(qcd_control_alternative.project("yaxis"))
        ttbar_btag_y, qcd_btag_ey = scale_to_bin_width(ttbar_control_alternative.project("yaxis"))
        signal_btag_y, qcd_btag_ey = scale_to_bin_width(signal_control_alternative.project("yaxis"))
        data_btag_y, data_btag_ey = scale_to_bin_width(data_hist_control_alternative.project("yaxis"))
        
        hep.histplot(qcd_btag_y, stack=True, histtype="fill", label="QCD")
        hep.histplot(ttbar_btag_y, stack=True, histtype="fill", label="TTbar")
        #background_plot_y.plot(stack=True, histtype="fill")
        hep.histplot(1 *signal_btag_y, stack=False, label="Signal")
        #data_btag_y.plot(histtype="errorbar", label="Data", color="black")
        hep.histplot(data_btag_y, yerr=data_btag_ey, histtype="errorbar", label="Data", color="black")
        
        hep.cms.text("Work in progress",loc=0)
        # lumiText = "$41.5 fb^{-1} (13 TeV)$"    
        hep.cms.lumitext(lumiText)
        plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
        plt.xlabel("Dijet Mass [GeV]")
        plt.legend()
        plt.savefig("mjj_control_alternative_pass_run2.png")
        plt.cla()
        plt.clf()
        
        plt.style.use([hep.style.CMS])
        plt.tight_layout()
        hep.histplot(data_btag_y / (qcd_btag_y + ttbar_btag_y),  label="Ratio")
        
        hep.cms.text("Work in progress",loc=0)   
        hep.cms.lumitext(lumi_text)
        plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
        plt.xlabel("Dijet Mass [GeV]")
        plt.legend()
        plt.savefig("mjj_ratio_pass_run2.png")
        plt.cla()
        plt.clf()
    
    # for i in range(3):
    #     with uproot.open("FittingArea/QCD17_{0}_b-tag.root".format(i)) as file:
    #         qcd_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #         qcd_signal.name = "QCD"
    #         qcd_control = file["mjjall_vs_mjjj_control_rebinned"].to_hist()
    #         qcd_control.name = "QCD"
    #         qcd_control_integral_hist = file["mjjall_vs_mjjj_control"].to_hist()
    #         print("QCD Control Integral yield: ", hist_yield(qcd_control_integral_hist))
    #         qcd_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
    #         qcd_control_alternative.name = "QCD"
    #         print("QCD yield: ", hist_yield(qcd_signal))
    #         # qcd_signal.project("trijet_mass").plot()
    #         ax = qcd_signal.project("xaxis").axes[0]
    #         cat = hist.axis.StrCategory(["QCD", "TTbar", "Signal"], name="cat")
    #         lumi_text = "$41.5 fb^{-1} (13 TeV)$"
    #         cms_text = "Work in progress"
    #         plot_hist(qcd_signal, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_qcd_signal_{0}_b-tag.png".format(i))
            
    #         print("QCD control yield: ", hist_yield(qcd_control))
    #         plot_hist(qcd_control, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_qcd_control_{0}_b-tag.png".format(i))
            
    #         print("QCD control alternative yield: ", hist_yield(qcd_control_alternative))
    #         plot_hist(qcd_control_alternative, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_qcd_control_alt_{0}_b-tag.png".format(i))
    #         # j3_hist_unfolded = file["unwrapped_mjjall_vs_mjjj"].to_hist()
    #         # plot_hist(j3_hist_unfolded, lumi_text, 
    #         #         cms_text, "Event count", 
    #         #         "Bin number", "mjj_vs_mjjj_qcd_unfolded.png")
            
    #     with uproot.open('FittingArea/XToHY_6b_2000_1100_{0}_b-tag.root'.format(i)) as file:
    #         signal_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #         signal_signal.name = "Signal"
    #         signal_control = file["mjjall_vs_mjjj_control_rebinned"].to_hist()
    #         signal_control.name = "Signal"
    #         signal_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
    #         signal_control_alternative.name = "Signal"
    #         print("signal yield: ", hist_yield(signal_signal))
    #         plot_hist(signal_signal, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_signal_signal_{0}_b-tag.png".format(i))
    #         print("signal control yield: ", hist_yield(signal_control))
    #         plot_hist(signal_control, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_signal_control_{0}_b-tag.png".format(i))
    #         print("signal control alt yield: ", hist_yield(signal_control_alternative))
    #         plot_hist(signal_control_alternative, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_signal_control_alt_{0}_b-tag.png".format(i))
            
    #     with uproot.open('background/scaled/JetHT17_{0}_b-tag.root'.format(i)) as file:
    #         data_hist_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #         data_hist_signal.name = "Data"
    #         data_hist_control = file["mjjall_vs_mjjj_control_rebinned"].to_hist()
    #         data_hist_control.name = "Data"
    #         data_hist_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
    #         data_hist_control_alternative.name = "Data"
    #         print("data control yield: ", hist_yield(data_hist_control))
            
    #     with uproot.open('FittingArea/TTbar17_{0}_b-tag.root'.format(i)) as file:
    #         ttbar_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
    #         ttbar_signal.name = "TTbar"
    #         ttbar_control = file["mjjall_vs_mjjj_control_rebinned"].to_hist()
    #         ttbar_control_integral_hist = file["mjjall_vs_mjjj_control"].to_hist()
    #         print("TTbar Integral yield: ", hist_yield(ttbar_control_integral_hist))
    #         ttbar_control.name = "TTbar"
    #         ttbar_control_alternative = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
    #         ttbar_control_alternative.name = "TTbar"
    #         print("ttbar yield: ", hist_yield(ttbar_signal))
    #         plot_hist(ttbar_signal, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_ttbar_signal_0_b-tag.png")
    #         print("ttbar control yield: ", hist_yield(ttbar_control))
    #         plot_hist(ttbar_control, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_ttbar_control_0_b-tag.png")
            
    #         print("ttbar control alt yield: ", hist_yield(ttbar_control_alternative))
    #         plot_hist(ttbar_control_alternative, lumi_text, 
    #                 cms_text, "Trijet Mass [GeV]", 
    #                 "Dijet Mass [GeV]", "mjj_vs_mjjj_ttbar_alt_control_0_b-tag.png")
            
    #         plt.style.use([hep.style.CMS])
    #         plt.tight_layout()
    #         qcd_0_btag_x, qcd_0_btag_ex = scale_to_bin_width(qcd_signal.project("xaxis"))
    #         ttbar_0_btag_x, ttbar_0_btag_ex = scale_to_bin_width(ttbar_signal.project("xaxis"))
    #         signal_0_btag_x, signal_0_btag_ex = scale_to_bin_width(signal_signal.project("xaxis"))
    #         data_0_btag_x, data_0_btag_ex = scale_to_bin_width(data_hist_signal.project("xaxis"))
            
    #         hep.histplot(qcd_0_btag_x, stack=True, histtype="fill", label="QCD")
    #         hep.histplot(ttbar_0_btag_x, stack=True, histtype="fill", label="TTbar")
    #         #background_plot_x.plot(stack=True, histtype="fill")
    #         hep.histplot(0.1 * signal_0_btag_x, stack=False, label="Signal")
    #         #data_0_btag_x.plot(histtype="errorbar", label="Data", color="black")
    #         # hep.histplot(data_0_btag_x, yerr=data_0_btag_ex, histtype="errorbar", label="Data", color="black")
            
    #         hep.cms.text("Work in progress",loc=0)   
    #         hep.cms.lumitext(lumi_text)
    #         plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #         plt.xlabel("Trijet Mass [GeV]")
    #         plt.legend()
    #         plt.savefig("mjjj_signal_{0}_b-tag.png".format(i))
    #         plt.cla()
    #         plt.clf()
            
    #         plt.style.use([hep.style.CMS])
    #         plt.tight_layout()
    #         qcd_0_btag_y, qcd_0_btag_ey = scale_to_bin_width(qcd_signal.project("yaxis"))
    #         ttbar_0_btag_y, qcd_0_btag_ey = scale_to_bin_width(ttbar_signal.project("yaxis"))
    #         signal_0_btag_y, qcd_0_btag_ey = scale_to_bin_width(signal_signal.project("yaxis"))
    #         data_0_btag_y, data_0_btag_ey = scale_to_bin_width(data_hist_signal.project("yaxis"))
            
    #         hep.histplot(qcd_0_btag_y, stack=True, histtype="fill", label="QCD")
    #         hep.histplot(ttbar_0_btag_y, stack=True, histtype="fill", label="TTbar")
    #         #background_plot_y.plot(stack=True, histtype="fill")
    #         hep.histplot(0.1 * signal_0_btag_y, stack=False, label="Signal")
    #         #data_0_btag_y.plot(histtype="errorbar", label="Data", color="black")
    #         #hep.histplot(data_0_btag_y, yerr=data_0_btag_ey, histtype="errorbar", label="Data", color="black")
            
    #         hep.cms.text("Work in progress",loc=0)
    #         lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #         hep.cms.lumitext(lumiText)
    #         plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #         plt.xlabel("Dijet Mass [GeV]")
    #         plt.legend()
    #         plt.savefig("mjj_signal_{0}_b-tag.png".format(i))
    #         plt.cla()
    #         plt.clf()
            
    #         plt.style.use([hep.style.CMS])
    #         plt.tight_layout()
    #         qcd_btag_x, qcd_btag_ex = scale_to_bin_width(qcd_control.project("xaxis"))
    #         ttbar_btag_x, ttbar_btag_ex = scale_to_bin_width(ttbar_control.project("xaxis"))
    #         signal_btag_x, signal_btag_ex = scale_to_bin_width(signal_control.project("xaxis"))
    #         data_btag_x, data_btag_ex = scale_to_bin_width(data_hist_control.project("xaxis"))
            
    #         hep.histplot(qcd_btag_x, stack=True, histtype="fill", label="QCD")
    #         hep.histplot(ttbar_btag_x, stack=True, histtype="fill", label="TTbar")
    #         #background_plot_x.plot(stack=True, histtype="fill")
    #         hep.histplot(0.1 * signal_btag_x, stack=False, label="Signal")
    #         #data_btag_x.plot(histtype="errorbar", label="Data", color="black")
    #         hep.histplot(data_btag_x, yerr=data_btag_ex, histtype="errorbar", label="Data", color="black")
            
    #         hep.cms.text("Work in progress",loc=0)   
    #         hep.cms.lumitext(lumi_text)
    #         plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #         plt.xlabel("Trijet Mass [GeV]")
    #         plt.legend()
    #         plt.savefig("mjjj_control_{0}_b-tag.png".format(i))
    #         plt.cla()
    #         plt.clf()
            
    #         plt.style.use([hep.style.CMS])
    #         plt.tight_layout()
    #         qcd_btag_y, qcd_btag_ey = scale_to_bin_width(qcd_control.project("yaxis"))
    #         ttbar_btag_y, qcd_btag_ey = scale_to_bin_width(ttbar_control.project("yaxis"))
    #         signal_btag_y, qcd_btag_ey = scale_to_bin_width(signal_control.project("yaxis"))
    #         data_btag_y, data_btag_ey = scale_to_bin_width(data_hist_control.project("yaxis"))
            
    #         hep.histplot(qcd_btag_y, stack=True, histtype="fill", label="QCD")
    #         hep.histplot(ttbar_btag_y, stack=True, histtype="fill", label="TTbar")
    #         #background_plot_y.plot(stack=True, histtype="fill")
    #         hep.histplot(0.1 * signal_btag_y, stack=False, label="Signal")
    #         #data_btag_y.plot(histtype="errorbar", label="Data", color="black")
    #         print(np.sqrt(data_btag_y.to_numpy()[0]), data_btag_ey)
    #         hep.histplot(data_btag_y, yerr=data_btag_ey, histtype="errorbar", label="Data", color="black")
            
    #         hep.cms.text("Work in progress",loc=0)
    #         lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #         hep.cms.lumitext(lumiText)
    #         plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #         plt.xlabel("Dijet Mass [GeV]")
    #         plt.legend()
    #         plt.savefig("mjj_control_{0}_b-tag.png".format(i))
    #         plt.cla()
    #         plt.clf()
            
    #         plt.style.use([hep.style.CMS])
    #         plt.tight_layout()
    #         qcd_btag_x, qcd_btag_ex = scale_to_bin_width(qcd_control_alternative.project("xaxis"))
    #         ttbar_btag_x, ttbar_btag_ex = scale_to_bin_width(ttbar_control_alternative.project("xaxis"))
    #         signal_btag_x, signal_btag_ex = scale_to_bin_width(signal_control_alternative.project("xaxis"))
    #         data_btag_x, data_btag_ex = scale_to_bin_width(data_hist_control_alternative.project("xaxis"))
            
    #         hep.histplot(qcd_btag_x, stack=True, histtype="fill", label="QCD")
    #         hep.histplot(ttbar_btag_x, stack=True, histtype="fill", label="TTbar")
    #         #background_plot_x.plot(stack=True, histtype="fill")
    #         hep.histplot(0.1 * signal_btag_x, stack=False, label="Signal")
    #         #data_btag_x.plot(histtype="errorbar", label="Data", color="black")
    #         hep.histplot(data_btag_x, yerr=data_btag_ex, histtype="errorbar", label="Data", color="black")
            
    #         hep.cms.text("Work in progress",loc=0)   
    #         hep.cms.lumitext(lumi_text)
    #         plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #         plt.xlabel("Trijet Mass [GeV]")
    #         plt.legend()
    #         plt.savefig("mjjj_control_alternative_{0}_b-tag.png".format(i))
    #         plt.cla()
    #         plt.clf()
            
    #         plt.style.use([hep.style.CMS])
    #         plt.tight_layout()
    #         qcd_btag_y, qcd_btag_ey = scale_to_bin_width(qcd_control_alternative.project("yaxis"))
    #         ttbar_btag_y, qcd_btag_ey = scale_to_bin_width(ttbar_control_alternative.project("yaxis"))
    #         signal_btag_y, qcd_btag_ey = scale_to_bin_width(signal_control_alternative.project("yaxis"))
    #         data_btag_y, data_btag_ey = scale_to_bin_width(data_hist_control_alternative.project("yaxis"))
            
    #         hep.histplot(qcd_btag_y, stack=True, histtype="fill", label="QCD")
    #         hep.histplot(ttbar_btag_y, stack=True, histtype="fill", label="TTbar")
    #         #background_plot_y.plot(stack=True, histtype="fill")
    #         hep.histplot(0.1 * signal_btag_y, stack=False, label="Signal")
    #         #data_btag_y.plot(histtype="errorbar", label="Data", color="black")
    #         hep.histplot(data_btag_y, yerr=data_btag_ey, histtype="errorbar", label="Data", color="black")
            
    #         hep.cms.text("Work in progress",loc=0)
    #         lumiText = "$41.5 fb^{-1} (13 TeV)$"    
    #         hep.cms.lumitext(lumiText)
    #         plt.ylabel(r"Event count/Bin width [GeV$^{-1}$]",horizontalalignment='right', y=1.0)
    #         plt.xlabel("Dijet Mass [GeV]")
    #         plt.legend()
    #         plt.savefig("mjj_control_alternative_{0}_b-tag.png".format(i))
    #         plt.cla()
    #         plt.clf()
        
        
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
    #     plt.savefig("mjj_vs_mjjj_qcd_1_b-tag.png")
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