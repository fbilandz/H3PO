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
import ROOT

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

def rpf(x, y):
    par0 = 9.05383125254
    par1 = -2.64730833027
    par2 = 0.327237764433
    return 0.01 * (par0 + par1 * x + par2 * y)

def rescale_by_rpf():
    DataFile = ROOT.TFile.Open("FittingArea/Jet_Run2_fail_2.root", "UPDATE")
    TTbarFile = ROOT.TFile.Open("FittingArea/TTbar_Run2_fail.root")
    data_hist_sr = DataFile.Get("mjjall_vs_mjjj_signal_rebinned")
    ttbar_hist_sr = TTbarFile.Get("mjjall_vs_mjjj_signal_rebinned")
    hRes = data_hist_sr.Clone("mjjall_vs_mjjj_signal_rebinned_bkg_estimated_pass")
    hRes.Reset()
    x_min, x_max = data_hist_sr.GetXaxis().GetXmin(), data_hist_sr.GetXaxis().GetXmax()
    y_min, y_max = data_hist_sr.GetYaxis().GetXmin(), data_hist_sr.GetYaxis().GetXmax()
    for j in range(1, data_hist_sr.GetNbinsY()+1):
        for i in range(1, data_hist_sr.GetNbinsX()+1):
            x_center = data_hist_sr.GetXaxis().GetBinCenter(i)
            y_center = data_hist_sr.GetYaxis().GetBinCenter(j)
            x = (x_center - x_min)/(x_max - x_min)
            y = (y_center - y_min)/(y_max - y_min)
            print(x_center, y_center, data_hist_sr.GetBinContent(i, j) * rpf(x, y))
            hRes.SetBinContent(i, j, (data_hist_sr.GetBinContent(i, j) - ttbar_hist_sr.GetBinContent(i, j)) * rpf(x, y) + ttbar_hist_sr.GetBinContent(i, j))
            # hRes.SetBinError(i, j, data_hist_sr.GetBinError(i, j)* rpf(x_center, y_center))
    
    DataFile.WriteObject(hRes, "mjjall_vs_mjjj_signal_rebinned_bkg_estimated_pass")
    print(hRes.Integral())
    
def generate_pdf():
    DataFile = ROOT.TFile.Open("FittingArea/Jet_Run2_fail_2.root", "UPDATE")
    data_hist_sr = DataFile.Get("mjjall_vs_mjjj_signal_rebinned_bkg_estimated_pass")
    hRes = data_hist_sr.Clone("mjjall_vs_mjjj_signal_rebinned_bkg_pdf")
    hRes.Scale(1/hRes.Integral())
    DataFile.WriteObject(hRes, "mjjall_vs_mjjj_signal_rebinned_bkg_pdf")
        
def generate_N_bkg(N):
    DataFile = ROOT.TFile.Open("FittingArea/Jet_Run2_fail_2.root", "UPDATE")
    data_hist_sr = DataFile.Get("mjjall_vs_mjjj_signal_rebinned_bkg_pdf")
    x = ROOT.TRandom()
    x.SetSeed(0)

    NBINS = data_hist_sr.GetNbinsY() * data_hist_sr.GetNbinsX()
    print(NBINS)
    pVals = ROOT.TH1F("pVals", "", NBINS, 1, NBINS + 1)
    suma = 0.
    tpair_tree = {}
    for j in range(1, data_hist_sr.GetNbinsY()+1):
        for i in range(1, data_hist_sr.GetNbinsX()+1):
            pVals.SetBinContent((j-1) * data_hist_sr.GetNbinsX() + i, suma)
            tpair_tree[(j-1) * data_hist_sr.GetNbinsX() + i] = (i, j)
            print(suma)
            suma += data_hist_sr.GetBinContent(i, j)
    
    hRes = data_hist_sr.Clone("mjjall_vs_mjjj_signal_rebinned_bkg_N_generated")
    hRes.Reset()
    for r in range(N):
        tbgVal = x.Uniform(1)
        px = pVals.FindFirstBinAbove(tbgVal) - 1
        # print(px, px%data_hist_sr.GetNbinsX(), px//data_hist_sr.GetNbinsY())
        if px == -2:
            px = 192
        pair = tpair_tree[px]
        x_center = data_hist_sr.GetXaxis().GetBinCenter(pair[0])
        y_center = data_hist_sr.GetYaxis().GetBinCenter(pair[1]) 
        hRes.Fill(x_center, y_center)
    
    DataFile.WriteObject(pVals, "mjjall_vs_mjjj_signal_rebinned_p_vals")
    DataFile.WriteObject(hRes, "mjjall_vs_mjjj_signal_rebinned_bkg_N_generated")
    
def rename_histograms():
    # DataFile = ROOT.TFile.Open("FittingArea/Jet_Run2_fail_2.root", "UPDATE")
    # data_hist_sr = DataFile.Get("mjjall_vs_mjjj_signal_rebinned")
    # hRes = data_hist_sr.Clone("mjjall_vs_mjjj_signal_rebinned_fail")
    # DataFile.WriteObject(hRes, "mjjall_vs_mjjj_signal_rebinned_fail")
    
    # data_hist_sr2 = DataFile.Get("mjjall_vs_mjjj_signal_rebinned_bkg_N_generated")
    # hRes2 = data_hist_sr2.Clone("mjjall_vs_mjjj_signal_rebinned_pass")
    # DataFile.WriteObject(hRes2, "mjjall_vs_mjjj_signal_rebinned_pass")
    
    # TTbarFile1 = ROOT.TFile.Open("FittingArea/TTbar_Run2_fail.root", "UPDATE")
    # data_hist_sr3 = TTbarFile1.Get("mjjall_vs_mjjj_signal_rebinned")
    # hRes3 = data_hist_sr3.Clone("mjjall_vs_mjjj_signal_rebinned_fail")
    # TTbarFile1.WriteObject(hRes3, "mjjall_vs_mjjj_signal_rebinned_fail")
    
    TTbarFile2 = ROOT.TFile.Open("FittingArea/TTbar_Run2_pass.root", "UPDATE")
    data_hist_sr4 = TTbarFile2.Get("mjjall_vs_mjjj_signal_rebinned")
    hRes4 = data_hist_sr4.Clone("mjjall_vs_mjjj_signal_rebinned_pass")
    TTbarFile2.WriteObject(hRes4, "mjjall_vs_mjjj_signal_rebinned_pass")
    
if __name__ == '__main__':
    # rescale_by_rpf()
    # generate_pdf()
    # generate_N_bkg(5860)
    
    rename_histograms()