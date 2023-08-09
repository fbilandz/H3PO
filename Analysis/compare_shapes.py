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

def normalize_hist(h, errors):
    integral = np.sum(np.sum(h.to_numpy()[0]))
    print(h.name, integral)
    h_res = Hist(h.axes[0])
    h_res.name = h.name
    h_res.label = h.label
    error_data = []

    for i in range(len(h.to_numpy()[0])):
        width = h.to_numpy()[1][i + 1] - h.to_numpy()[1][i]
        h_res[i] = h.to_numpy()[0][i]/ width / integral * 100 
        error = errors[i]/width/ integral * 100 
        error_data.append(error)
    return h_res, error_data

def plot_templates():
    qcd_x_signal = []
    
    qcd_x_control = []
    qcd_y_signal = []
    qcd_y_control = []
    
    ttbar_x_signal = []
    ttbar_x_control = []
    ttbar_y_signal = []
    ttbar_y_control = []
    
    data_x_signal = []
    data_x_control = []
    data_y_signal = []
    data_y_control = []
    
    qcd_file = ROOT.TFile.Open("FittingArea/QCD_Run2_fail.root")
    qcd_signal_projx = qcd_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionX()
    qcd_signal_projy = qcd_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionY()
    signal_x = []
    signal_ex = []
    signal_y = []
    signal_ey = []
    for i in range(qcd_signal_projx.GetNbinsX()):
        signal_x.append(qcd_signal_projx.GetBinContent(i + 1))
        signal_ex.append(qcd_signal_projx.GetBinError(i + 1))
        
    for i in range(qcd_signal_projy.GetNbinsX()):
        signal_y.append(qcd_signal_projy.GetBinContent(i + 1))
        signal_ey.append(qcd_signal_projy.GetBinError(i + 1))   
    
    qcd_control_alternative_projx = qcd_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionX()
    qcd_control_alternative_projy = qcd_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionY()
    control_alternative_x = []
    control_alternative_ex = []
    control_alternative_y = []
    control_alternative_ey = []
    for i in range(qcd_control_alternative_projx.GetNbinsX()):
        control_alternative_x.append(qcd_control_alternative_projx.GetBinContent(i + 1))
        control_alternative_ex.append(qcd_control_alternative_projx.GetBinError(i + 1))
        
    for i in range(qcd_control_alternative_projy.GetNbinsX()):
        control_alternative_y.append(qcd_control_alternative_projy.GetBinContent(i + 1))
        control_alternative_ey.append(qcd_control_alternative_projy.GetBinError(i + 1))
        
    with uproot.open("FittingArea/QCD_Run2_fail.root") as file:
        qcd_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        qcd_signal.name = "QCD"
        qcd_signal_x, qcd_signal_ex = normalize_hist(qcd_signal.project('xaxis'), signal_ex)
        qcd_signal_y, qcd_signal_ey = normalize_hist(qcd_signal.project('yaxis'), signal_ey)
        qcd_x_signal.append([qcd_signal_x, qcd_signal_ex])
        qcd_y_signal.append([qcd_signal_y, qcd_signal_ey])
        qcd_control = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        qcd_control.name = "QCD"
        qcd_control_x, qcd_control_ex = normalize_hist(qcd_control.project('xaxis'), control_alternative_ex)
        qcd_control_y, qcd_control_ey = normalize_hist(qcd_control.project('yaxis'), control_alternative_ey)
        qcd_x_control.append([qcd_control_x, qcd_control_ex])
        qcd_y_control.append([qcd_control_y, qcd_control_ey])
        
    ttbar_file = ROOT.TFile.Open("FittingArea/TTbar_Run2_fail.root")
    ttbar_signal_projx = ttbar_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionX()
    ttbar_signal_projy = ttbar_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionY()
    print("ttbar integral", ttbar_file.Get("mjjall_vs_mjjj_signal_rebinned").Integral())
    
    signal_x = []
    signal_ex = []
    signal_y = []
    signal_ey = []
    for i in range(ttbar_signal_projx.GetNbinsX()):
        signal_x.append(ttbar_signal_projx.GetBinContent(i + 1))
        signal_ex.append(ttbar_signal_projx.GetBinError(i + 1))
        
    for i in range(ttbar_signal_projy.GetNbinsX()):
        signal_y.append(ttbar_signal_projy.GetBinContent(i + 1))
        signal_ey.append(ttbar_signal_projy.GetBinError(i + 1))   

    ttbar_control_alternative_projx = ttbar_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionX()
    ttbar_control_alternative_projy = ttbar_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionY()
    print("ttbar integral", ttbar_file.Get("unwrapped_mjjall_vs_mjjj_control_alternative").Integral())
    control_alternative_x = []
    control_alternative_ex = []
    control_alternative_y = []
    control_alternative_ey = []
    for i in range(ttbar_control_alternative_projx.GetNbinsX()):
        control_alternative_x.append(ttbar_control_alternative_projx.GetBinContent(i + 1))
        control_alternative_ex.append(ttbar_control_alternative_projx.GetBinError(i + 1))
        
    for i in range(ttbar_control_alternative_projy.GetNbinsX()):
        control_alternative_y.append(ttbar_control_alternative_projy.GetBinContent(i + 1))
        control_alternative_ey.append(ttbar_control_alternative_projy.GetBinError(i + 1))
    
    
    with uproot.open("FittingArea/TTbar_Run2_fail.root") as file:
        ttbar_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        ttbar_signal.name = "TTbar"
        ttbar_signal_x, ttbar_signal_ex = normalize_hist(ttbar_signal.project('xaxis'), signal_ex)
        ttbar_signal_y, ttbar_signal_ey = normalize_hist(ttbar_signal.project('yaxis'), signal_ey)
        ttbar_x_signal.append([ttbar_signal_x, ttbar_signal_ex])
        ttbar_y_signal.append([ttbar_signal_y, ttbar_signal_ey])
        ttbar_control = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        ttbar_control.name = "TTbar"
        ttbar_control_x, ttbar_control_ex = normalize_hist(ttbar_control.project('xaxis'), control_alternative_ex)
        ttbar_control_y, ttbar_control_ey = normalize_hist(ttbar_control.project('yaxis'), control_alternative_ey)
        ttbar_x_control.append([ttbar_control_x, ttbar_control_ex])
        ttbar_y_control.append([ttbar_control_y, ttbar_control_ey])
    
    data_file = ROOT.TFile.Open("FittingArea/JetHT_Run2_fail.root")
    data_signal_projx = data_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionX()
    data_signal_projy = data_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionY()
    signal_x = []
    signal_ex = []
    signal_y = []
    signal_ey = []
    for i in range(data_signal_projx.GetNbinsX()):
        signal_x.append(data_signal_projx.GetBinContent(i + 1))
        signal_ex.append(data_signal_projx.GetBinError(i + 1))
        
    for i in range(data_signal_projy.GetNbinsX()):
        signal_y.append(data_signal_projy.GetBinContent(i + 1))
        signal_ey.append(data_signal_projy.GetBinError(i + 1))   

    data_control_alternative_projx = data_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionX()
    data_control_alternative_projy = data_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionY()
    control_alternative_x = []
    control_alternative_ex = []
    control_alternative_y = []
    control_alternative_ey = []
    for i in range(data_control_alternative_projx.GetNbinsX()):
        control_alternative_x.append(data_control_alternative_projx.GetBinContent(i + 1))
        control_alternative_ex.append(data_control_alternative_projx.GetBinError(i + 1))
        
    for i in range(data_control_alternative_projy.GetNbinsX()):
        control_alternative_y.append(data_control_alternative_projy.GetBinContent(i + 1))
        control_alternative_ey.append(data_control_alternative_projy.GetBinError(i + 1))
    
    with uproot.open("FittingArea/JetHT_Run2_fail.root") as file:
        data_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        data_signal.name = "Data"
        data_signal_x, data_signal_ex = normalize_hist(data_signal.project('xaxis'), signal_ex)
        data_signal_y, data_signal_ey = normalize_hist(data_signal.project('yaxis'), signal_ey)
        data_x_signal.append([data_signal_x, data_signal_ex])
        data_y_signal.append([data_signal_y, data_signal_ey])
        data_control = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        data_control.name = "Data"
        data_control_x, data_control_ex = normalize_hist(data_control.project('xaxis'), control_alternative_ex)
        data_control_y, data_control_ey = normalize_hist(data_control.project('yaxis'), control_alternative_ey)
        data_x_control.append([data_control_x, data_control_ex])
        data_y_control.append([data_control_y, data_control_ey])
        
    print(np.array(data_control_ex))
    print(qcd_control_x.to_numpy())
    err = np.sqrt((np.array(data_control_ex)/(qcd_control_x.to_numpy()[0] + ttbar_control_x.to_numpy()[0]))**2 + (data_control_x.to_numpy()[0] * np.array(qcd_control_ex)/(qcd_control_x.to_numpy()[0] + ttbar_control_x.to_numpy()[0])**2)**2 + (data_control_x.to_numpy()[0] * np.array(ttbar_control_ex)/(qcd_control_x.to_numpy()[0] + ttbar_control_x.to_numpy()[0])**2)**2)
    print(err)
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hep.histplot(data_control_x / (qcd_control_x + ttbar_control_x), yerr=err, label="Ratio")
    
    hep.cms.text("Work in progress",loc=0)   
    hep.cms.lumitext("$138 fb^{-1} (13 TeV)$")
    plt.ylabel(r"Data/Background [a.u.]",horizontalalignment='right', y=1.0)
    plt.xlabel("Trijet Mass [GeV]")
    plt.legend()
    plt.savefig("mjjj_ratio_control_fail_run2.png")
    plt.cla()
    plt.clf()
    
    err = np.sqrt((np.array(data_control_ex)/(qcd_control_x.to_numpy()[0] + ttbar_control_x.to_numpy()[0]))**2 + (data_control_x.to_numpy()[0] * np.array(qcd_control_ex)/(qcd_control_x.to_numpy()[0] + ttbar_control_x.to_numpy()[0])**2)**2 + (data_control_x.to_numpy()[0] * np.array(ttbar_control_ex)/(qcd_control_x.to_numpy()[0] + ttbar_control_x.to_numpy()[0])**2)**2)
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hep.histplot(data_control_x / (qcd_control_x + ttbar_control_x), yerr=err, label="Ratio")
    
    hep.cms.text("Work in progress",loc=0)   
    hep.cms.lumitext("$138 fb^{-1} (13 TeV)$")
    plt.ylabel(r"Data/Background [a.u.]",horizontalalignment='right', y=1.0)
    plt.xlabel("Trijet Mass [GeV]")
    plt.legend()
    plt.savefig("mjjj_ratio_control_fail_run2.png")
    plt.cla()
    plt.clf()
    
    err = np.sqrt((np.array(data_control_ey)/(qcd_control_y.to_numpy()[0] + ttbar_control_y.to_numpy()[0]))**2 + (data_control_y.to_numpy()[0] * np.array(qcd_control_ey)/(qcd_control_y.to_numpy()[0] + ttbar_control_y.to_numpy()[0])**2)**2 + (data_control_y.to_numpy()[0] * np.array(ttbar_control_ey)/(qcd_control_y.to_numpy()[0] + ttbar_control_y.to_numpy()[0])**2)**2)
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hep.histplot(data_control_y / (qcd_control_y + ttbar_control_y), yerr=err, label="Ratio")
    
    hep.cms.text("Work in progress",loc=0)   
    hep.cms.lumitext("$138 fb^{-1} (13 TeV)$")
    plt.ylabel(r"Data/Background [a.u.]",horizontalalignment='right', y=1.0)
    plt.xlabel("Dijet Mass [GeV]")
    plt.legend()
    plt.savefig("mjj_ratio_control_fail_run2.png")
    plt.cla()
    plt.clf()
    
    
    qcd_file = ROOT.TFile.Open("FittingArea/QCD_Run2_pass.root")
    qcd_signal_projx = qcd_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionX()
    qcd_signal_projy = qcd_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionY()
    signal_x = []
    signal_ex = []
    signal_y = []
    signal_ey = []
    for i in range(qcd_signal_projx.GetNbinsX()):
        signal_x.append(qcd_signal_projx.GetBinContent(i + 1))
        signal_ex.append(qcd_signal_projx.GetBinError(i + 1))
        
    for i in range(qcd_signal_projy.GetNbinsX()):
        signal_y.append(qcd_signal_projy.GetBinContent(i + 1))
        signal_ey.append(qcd_signal_projy.GetBinError(i + 1))   
    
    qcd_control_alternative_projx = qcd_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionX()
    qcd_control_alternative_projy = qcd_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionY()
    control_alternative_x = []
    control_alternative_ex = []
    control_alternative_y = []
    control_alternative_ey = []
    for i in range(qcd_control_alternative_projx.GetNbinsX()):
        control_alternative_x.append(qcd_control_alternative_projx.GetBinContent(i + 1))
        control_alternative_ex.append(qcd_control_alternative_projx.GetBinError(i + 1))
        
    for i in range(qcd_control_alternative_projy.GetNbinsX()):
        control_alternative_y.append(qcd_control_alternative_projy.GetBinContent(i + 1))
        control_alternative_ey.append(qcd_control_alternative_projy.GetBinError(i + 1))
        
    with uproot.open("FittingArea/QCD_Run2_pass.root") as file:
        qcd_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        qcd_signal.name = "QCD"
        qcd_signal_x, qcd_signal_ex = normalize_hist(qcd_signal.project('xaxis'), signal_ex)
        qcd_signal_y, qcd_signal_ey = normalize_hist(qcd_signal.project('yaxis'), signal_ey)
        qcd_x_signal.append([qcd_signal_x, qcd_signal_ex])
        qcd_y_signal.append([qcd_signal_y, qcd_signal_ey])
        qcd_control = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        qcd_control.name = "QCD"
        qcd_control_x, qcd_control_ex = normalize_hist(qcd_control.project('xaxis'), control_alternative_ex)
        qcd_control_y, qcd_control_ey = normalize_hist(qcd_control.project('yaxis'), control_alternative_ey)
        qcd_x_control.append([qcd_control_x, qcd_control_ex])
        qcd_y_control.append([qcd_control_y, qcd_control_ey])
        
    ttbar_file = ROOT.TFile.Open("FittingArea/TTbar_Run2_pass.root")
    ttbar_signal_projx = ttbar_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionX()
    ttbar_signal_projy = ttbar_file.Get("mjjall_vs_mjjj_signal_rebinned").ProjectionY()
    print("ttbar integral", ttbar_file.Get("unwrapped_mjjall_vs_mjjj_signal").Integral())
    signal_x = []
    signal_ex = []
    signal_y = []
    signal_ey = []
    for i in range(ttbar_signal_projx.GetNbinsX()):
        signal_x.append(ttbar_signal_projx.GetBinContent(i + 1))
        signal_ex.append(ttbar_signal_projx.GetBinError(i + 1))
        
    for i in range(ttbar_signal_projy.GetNbinsX()):
        signal_y.append(ttbar_signal_projy.GetBinContent(i + 1))
        signal_ey.append(ttbar_signal_projy.GetBinError(i + 1))   

    ttbar_control_alternative_projx = ttbar_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionX()
    ttbar_control_alternative_projy = ttbar_file.Get("mjjall_vs_mjjj_control_alternative_rebinned").ProjectionY()
    print("ttbar integral", ttbar_file.Get("unwrapped_mjjall_vs_mjjj_control_alternative").Integral())
    control_alternative_x = []
    control_alternative_ex = []
    control_alternative_y = []
    control_alternative_ey = []
    for i in range(ttbar_control_alternative_projx.GetNbinsX()):
        control_alternative_x.append(ttbar_control_alternative_projx.GetBinContent(i + 1))
        control_alternative_ex.append(ttbar_control_alternative_projx.GetBinError(i + 1))
        
    for i in range(ttbar_control_alternative_projy.GetNbinsX()):
        control_alternative_y.append(ttbar_control_alternative_projy.GetBinContent(i + 1))
        control_alternative_ey.append(ttbar_control_alternative_projy.GetBinError(i + 1))
    
    with uproot.open("FittingArea/TTbar_Run2_pass.root") as file:
        ttbar_signal = file["mjjall_vs_mjjj_signal_rebinned"].to_hist()
        ttbar_signal.name = "TTbar"
        ttbar_signal_x, ttbar_signal_ex = normalize_hist(ttbar_signal.project('xaxis'), signal_ex)
        ttbar_signal_y, ttbar_signal_ey = normalize_hist(ttbar_signal.project('yaxis'), signal_ey)
        ttbar_x_signal.append([ttbar_signal_x, ttbar_signal_ex])
        ttbar_y_signal.append([ttbar_signal_y, ttbar_signal_ey])
        ttbar_control = file["mjjall_vs_mjjj_control_alternative_rebinned"].to_hist()
        ttbar_control.name = "TTbar"
        ttbar_control_x, ttbar_control_ex = normalize_hist(ttbar_control.project('xaxis'), control_alternative_ex)
        ttbar_control_y, ttbar_control_ey = normalize_hist(ttbar_control.project('yaxis'), control_alternative_ey)
        ttbar_x_control.append([ttbar_control_x, ttbar_control_ex])
        ttbar_y_control.append([ttbar_control_y, ttbar_control_ey])
            
        # qcd_file = ROOT.TFile.Open("FittingArea/QCD17_{0}_b-tag.root".format(i))
        # qcd_signal = qcd_file.Get("mjjall_vs_mjjj_signal_rebinned")
        # qcd_signal.Plot()
    qcd_signal_pass_x = qcd_x_signal[1][0]
    qcd_signal_pass_ex = qcd_x_signal[1][1]
    qcd_signal_fail_x = qcd_x_signal[0][0]
    qcd_signal_fail_ex = qcd_x_signal[0][1]
    
    err = np.sqrt((np.array(qcd_signal_pass_ex)/(qcd_signal_fail_x.to_numpy()[0]))**2 + (qcd_signal_pass_x.to_numpy()[0] * np.array(qcd_signal_fail_ex)/(qcd_signal_fail_x.to_numpy()[0])**2)**2)
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hep.histplot(qcd_signal_pass_x / qcd_signal_fail_x, yerr=err, label="Ratio")
    
    hep.cms.text("Work in progress",loc=0)   
    hep.cms.lumitext("$138 fb^{-1} (13 TeV)$")
    plt.ylabel(r"Pass/Fail [a.u.]",horizontalalignment='right', y=1.0)
    plt.xlabel("Trijet Mass [GeV]")
    plt.legend()
    plt.savefig("mjjj_ratio_pf_signal_run2.png")
    plt.cla()
    plt.clf()
    
    qcd_signal_pass_y = qcd_y_signal[1][0]
    qcd_signal_pass_ey = qcd_y_signal[1][1]
    qcd_signal_fail_y = qcd_y_signal[0][0]
    qcd_signal_fail_ey = qcd_y_signal[0][1]
    err = np.sqrt((np.array(qcd_signal_pass_ey)/(qcd_signal_fail_y.to_numpy()[0]))**2 + (qcd_signal_pass_y.to_numpy()[0] * np.array(qcd_signal_fail_ey)/(qcd_signal_fail_y.to_numpy()[0])**2)**2)
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hep.histplot(qcd_signal_pass_y / qcd_signal_fail_y, yerr=err, label="Ratio")
    
    hep.cms.text("Work in progress",loc=0)   
    hep.cms.lumitext("$138 fb^{-1} (13 TeV)$")
    plt.ylabel(r"Pass/Fail[a.u.]",horizontalalignment='right', y=1.0)
    plt.xlabel("Dijet Mass [GeV]")
    plt.legend()
    plt.savefig("mjj_ratio_pf_signal_run2.png")
    plt.cla()
    plt.clf()
    
    
    
    qcd_control_fail_x = qcd_x_control[0][0]
    qcd_control_fail_ex = qcd_x_control[0][1]
    qcd_control_pass_x = qcd_x_control[1][0]
    qcd_control_pass_ex = qcd_x_control[1][1]
    err = np.sqrt((np.array(qcd_control_pass_ex)/(qcd_control_fail_x.to_numpy()[0]))**2 + (qcd_control_pass_x.to_numpy()[0] * np.array(qcd_control_fail_ex)/(qcd_control_fail_x.to_numpy()[0])**2)**2)
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hep.histplot(qcd_control_pass_x / qcd_control_fail_x, yerr=err, label="Ratio")
    
    hep.cms.text("Work in progress",loc=0)   
    hep.cms.lumitext("$138 fb^{-1} (13 TeV)$")
    plt.ylabel(r"Pass/Fail [a.u.]",horizontalalignment='right', y=1.0)
    plt.xlabel("Trijet Mass [GeV]")
    plt.legend()
    plt.savefig("mjjj_ratio_pf_control_run2.png")
    plt.cla()
    plt.clf()
    
    
    qcd_control_fail_y = qcd_y_control[0][0]
    qcd_control_fail_ey = qcd_y_control[0][1]
    qcd_control_pass_y = qcd_y_control[1][0]
    qcd_control_pass_ey = qcd_y_control[1][1]
    err = np.sqrt((np.array(qcd_control_pass_ey)/(qcd_control_fail_y.to_numpy()[0]))**2 + (qcd_control_pass_y.to_numpy()[0] * np.array(qcd_control_fail_ey)/(qcd_control_fail_y.to_numpy()[0])**2)**2)
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hep.histplot(qcd_control_pass_y / qcd_control_fail_y, yerr=err, label="Ratio")
    
    hep.cms.text("Work in progress",loc=0)   
    hep.cms.lumitext("$138 fb^{-1} (13 TeV)$")
    plt.ylabel(r"Pass/Fail [a.u.]",horizontalalignment='right', y=1.0)
    plt.xlabel("Dijet Mass [GeV]")
    plt.legend()
    plt.savefig("mjj_ratio_pf_control_run2.png")
    plt.cla()
    plt.clf()
    
    ttbar_control_fail_x = ttbar_x_control[0][0]
    ttbar_control_fail_ex = ttbar_x_control[0][1]
    ttbar_control_pass_x = ttbar_x_control[1][0]
    ttbar_control_pass_ex = ttbar_x_control[1][1]
    err = np.sqrt((np.array(ttbar_control_pass_ex)/(ttbar_control_fail_x.to_numpy()[0]))**2 + (ttbar_control_pass_x.to_numpy()[0] * np.array(ttbar_control_fail_ex)/(ttbar_control_fail_x.to_numpy()[0])**2)**2)
    plt.style.use([hep.style.CMS])
    plt.tight_layout()
    hep.histplot(ttbar_control_pass_x / ttbar_control_fail_x, yerr=err, label="Ratio")
    
    hep.cms.text("Work in progress",loc=0)   
    hep.cms.lumitext("$138 fb^{-1} (13 TeV)$")
    plt.ylabel(r"Pass/Fail [a.u.]",horizontalalignment='right', y=1.0)
    plt.xlabel("Dijet Mass [GeV]")
    plt.legend()
    plt.savefig("mjjj_ratio_pf_control_ttbar_run2.png")
    plt.cla()
    plt.clf()
    for i in [qcd_x_signal, qcd_x_control, qcd_y_signal, qcd_y_control, 
        ttbar_x_signal, ttbar_x_control, ttbar_y_signal, ttbar_y_control]:
        plt.style.use([hep.style.CMS])
        f, axs = plt.subplots(2,1, sharex=True, sharey=False,gridspec_kw={'height_ratios': [4, 1],'hspace': 0.05})
        axs = axs.flatten()
        plt.sca(axs[0])
        plt.tight_layout()
        lumiText = "$138 fb^{-1} (13 TeV)$"    
        hep.cms.lumitext(lumiText)
        hep.cms.text("Work in progress",loc=0)
        hep.histplot(i[0][0], yerr=i[0][1], ax=axs[0], histtype="step", label="Fail")
        hep.histplot(i[1][0], yerr=i[1][1], ax=axs[0], histtype="step", label="Pass")
        axs[0].set_ylabel("N/Bin Width [a.u.]",horizontalalignment='right', y=1.0)
        axs[0].set_xlabel("")
        fail_x = i[0][0]
        fail_ex = i[0][1]
        pass_x = i[1][0]
        pass_ex = i[1][1]
        err = np.sqrt((np.array(pass_ex)/(fail_x.to_numpy()[0]))**2 + (pass_x.to_numpy()[0] * np.array(fail_ex)/(fail_x.to_numpy()[0])**2)**2)
        
        plt.sca(axs[1])#switch to lower pad
        
        hep.histplot(pass_x/fail_x, yerr=err, ax=axs[1],linewidth=1,histtype="step")
        axs[1].set_ylim([0.5,1.5])
        if "ttbar" in [ z for z, j in locals().items() if np.array_equal(j, i)][0]:
            axs[1].set_ylim([0.7,1.3])
            if "_x_signal" in [ z for z, j in locals().items() if np.array_equal(j, i)][0]:
                axs[1].set_ylim([0.65,1.3])
        elif "signal" in [ z for z, j in locals().items() if np.array_equal(j, i)][0]:
            axs[1].set_ylim([0.4,1.7])
        axs[1].set_ylabel("Pass/Fail")
        axs[1].set_xlabel("Trijet Mass [GeV]")
        print(i)
        print([ z for z, j in locals().items() if np.array_equal(j, i)][0])
        plt.xlim([800, 4000])
        if "_y_" in [ z for z, j in locals().items() if np.array_equal(j, i)][0]:
            axs[1].set_xlabel("Dijet Mass [GeV]")
            plt.xlim([300, 2000])
        axs[0].legend()
        plt.savefig("compare_{0}_Run2.png".format([ z for z, j in locals().items() if np.array_equal(j, i)][0]))
        plt.cla()
        plt.clf()
        
if __name__ == '__main__':
    plot_templates()    
    