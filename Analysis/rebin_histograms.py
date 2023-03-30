import ROOT
import numpy as np

def rebinHisto(hModel,hToRebin,name,scale=1.0):
    hRes = hModel.Clone(name)
    hRes.Reset()
    xaxis = hToRebin.GetXaxis()
    yaxis = hToRebin.GetYaxis()
    xaxis_re = hRes.GetXaxis()
    yaxis_re = hRes.GetYaxis()
    for i in range(1,hToRebin.GetNbinsX()+1):
        for j in range(1,hToRebin.GetNbinsY()+1):
            x = xaxis.GetBinCenter(i)
            y = yaxis.GetBinCenter(j)
            i_re = xaxis_re.FindBin(x)
            j_re = yaxis_re.FindBin(y)
            value = hToRebin.GetBinContent(i,j)
            err = hToRebin.GetBinError(i,j)
            err_re = np.sqrt(hRes.GetBinError(i_re,j_re)*hRes.GetBinError(i_re,j_re)+err*err)
            hRes.Fill(x,y,value)
            hRes.SetBinError(i_re,j_re,err_re)
    hRes.Scale(scale)
    hRes.SetDirectory(0)
    return hRes

def calculate_non_zero_points_y(h):
    non_zero_points_y = []
    for j in range(1,h.GetNbinsY()+1):
        for i in range(1,h.GetNbinsX()+1):
            if h.GetBinContent(i, j) > 0:
                non_zero_points_y.append(i)
                break
            if i == h.GetNbinsX():
                non_zero_points_y.append(i)
    return non_zero_points_y

def calculate_required_bins(len_x, len_y, non_zero_points_y):
    required_bins = 0
    for j in range(len_y):
        required_bins += len_x + 1 - non_zero_points_y[j]
    return required_bins

def unwrap_2d_into_1d(h, name, non_zero_points_y, required_bins):
    counter = 1
    hRes = ROOT.TH1F(name, name, int(required_bins), 0, required_bins)
    for j in range(1,h.GetNbinsY()+1):
        for i in range(non_zero_points_y[j-1], h.GetNbinsX()+1):
            if h.GetBinContent(i, j) > 0:
                hRes.SetBinContent(counter, h.GetBinContent(i, j))
                hRes.SetBinError(counter, h.GetBinError(i, j))
            else:
                hRes.SetBinContent(counter, 1)
                hRes.SetBinError(counter, 1)
            counter += 1
    return hRes      

def create_dummy_unwrapped(hModel, name):
    hRes = hModel.Clone(name)
    hRes.Reset()
    for i in range(1,hRes.GetNbinsX()+1):
        hRes.SetBinContent(i, 1)
    return hRes
            
            
def rebin_histograms(n_of_tagged_jets=0):
    QCDFile = ROOT.TFile.Open("background/scaled/QCD17_{0}_b-tag.root".format(n_of_tagged_jets), "UPDATE")
    TTbarFile = ROOT.TFile.Open("background/scaled/TTbar17_{0}_b-tag.root".format(n_of_tagged_jets),"UPDATE")
    SignalFile = ROOT.TFile.Open("signal/scaled/XToHY_6b_2000_1100_{0}_b-tag.root".format(n_of_tagged_jets) ,"UPDATE")
    JetHTFile = ROOT.TFile.Open("background/scaled/JetHT17_{0}_b-tag.root".format(n_of_tagged_jets) ,"UPDATE")
    TwoDRebinnedEdgesX = [800.0, 900.0, 1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0, 1600.0, 1700.0, 1800.0, 1900.0, 2000.0, 2200.0, 2500.0, 3000.0, 4000.0]
    TwoDRebinnedEdgesY = [300.0, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000.0]
    TwoDRebinnedModel = ROOT.TH2F("TwoDRebinnedModel", "2D Rebinned Model", 
                                len(TwoDRebinnedEdgesX)-1, np.array(TwoDRebinnedEdgesX), 
                                len(TwoDRebinnedEdgesY)-1, np.array(TwoDRebinnedEdgesY))
    for region in ['signal', 'control', 'control_alternative']:
        qcd_mjjall_vs_mjjj_rebinned = rebinHisto(TwoDRebinnedModel, QCDFile.Get("mjjall_vs_mjjj_{0}".format(region)), "mjjall_vs_mjjj_{0}_rebinned".format(region))
        QCDFile.WriteObject(qcd_mjjall_vs_mjjj_rebinned, "mjjall_vs_mjjj_{0}_rebinned".format(region))
        
        ttbar_mjjall_vs_mjjj_rebinned = rebinHisto(TwoDRebinnedModel, TTbarFile.Get("mjjall_vs_mjjj_{0}".format(region)), "mjjall_vs_mjjj_{0}_rebinned".format(region))
        TTbarFile.WriteObject(ttbar_mjjall_vs_mjjj_rebinned, "mjjall_vs_mjjj_{0}_rebinned".format(region))
        
        qcd_non_zero_points_y = calculate_non_zero_points_y(qcd_mjjall_vs_mjjj_rebinned)
        ttbar_non_zero_points_y = calculate_non_zero_points_y(ttbar_mjjall_vs_mjjj_rebinned)
        non_zero_points_y = np.minimum(qcd_non_zero_points_y, ttbar_non_zero_points_y)
        required_bins = calculate_required_bins(len(TwoDRebinnedEdgesX) - 1, len(TwoDRebinnedEdgesY) - 1, non_zero_points_y)
        
        unwrapped_qcd_mjjall_vs_mjjj = unwrap_2d_into_1d(qcd_mjjall_vs_mjjj_rebinned, "unwrapped_mjjall_vs_mjjj_{0}".format(region), non_zero_points_y, required_bins)
        QCDFile.WriteObject(unwrapped_qcd_mjjall_vs_mjjj, "unwrapped_mjjall_vs_mjjj_{0}".format(region))
        unwrapped_ttbar_mjjall_vs_mjjj = unwrap_2d_into_1d(ttbar_mjjall_vs_mjjj_rebinned, "unwrapped_mjjall_vs_mjjj_{0}".format(region), non_zero_points_y, required_bins)
        TTbarFile.WriteObject(unwrapped_ttbar_mjjall_vs_mjjj, "unwrapped_mjjall_vs_mjjj_{0}".format(region))
        
        jet_ht_mjjall_vs_mjjj_rebinned = rebinHisto(TwoDRebinnedModel, JetHTFile.Get("mjjall_vs_mjjj_{0}".format(region)), "mjjall_vs_mjjj_{0}_rebinned".format(region))
        JetHTFile.WriteObject(jet_ht_mjjall_vs_mjjj_rebinned, "mjjall_vs_mjjj_{0}_rebinned".format(region))
        unwrapped_jet_ht_mjjall_vs_mjjj = unwrap_2d_into_1d(jet_ht_mjjall_vs_mjjj_rebinned, "unwrapped_mjjall_vs_mjjj_{0}".format(region), non_zero_points_y, required_bins)
        JetHTFile.WriteObject(unwrapped_jet_ht_mjjall_vs_mjjj, "unwrapped_mjjall_vs_mjjj_{0}".format(region))
        
        signal_mjjall_vs_mjjj_rebinned = rebinHisto(TwoDRebinnedModel, SignalFile.Get("mjjall_vs_mjjj_{0}".format(region)), "mjjall_vs_mjjj_{0}_rebinned".format(region))
        SignalFile.WriteObject(signal_mjjall_vs_mjjj_rebinned, "mjjall_vs_mjjj_{0}_rebinned".format(region))
        unwrapped_signal_mjjall_vs_mjjj = unwrap_2d_into_1d(signal_mjjall_vs_mjjj_rebinned, "unwrapped_mjjall_vs_mjjj_{0}".format(region), non_zero_points_y, required_bins)
        SignalFile.WriteObject(unwrapped_signal_mjjall_vs_mjjj, "unwrapped_mjjall_vs_mjjj_{0}".format(region))
        dummy_unwrapped_signal = create_dummy_unwrapped(unwrapped_signal_mjjall_vs_mjjj, "dummy_hist")
        SignalFile.WriteObject(dummy_unwrapped_signal, "unwrapped_dummy_signal")
        
    # qcd_mjjall_vs_mjjj_control_rebinned = rebinHisto(TwoDRebinnedModel, QCDFile.Get("mjjall_vs_mjjj_control"), "mjjall_vs_mjjj_control_rebinned")
    # QCDFile.WriteObject(qcd_mjjall_vs_mjjj_control_rebinned, "mjjall_vs_mjjj_control_rebinned")
    
    # ttbar_mjjall_vs_mjjj_control_rebinned = rebinHisto(TwoDRebinnedModel, TTbarFile.Get("mjjall_vs_mjjj_control"), "mjjall_vs_mjjj_control_rebinned")
    # TTbarFile.WriteObject(ttbar_mjjall_vs_mjjj_control_rebinned, "mjjall_vs_mjjj_control_rebinned")
    
    # qcd_non_zero_points_y_control = calculate_non_zero_points_y(qcd_mjjall_vs_mjjj_control_rebinned)
    # ttbar_non_zero_points_y_control = calculate_non_zero_points_y(ttbar_mjjall_vs_mjjj_control_rebinned)
    # non_zero_points_y = np.minimum(qcd_non_zero_points_y_control, ttbar_non_zero_points_y_control)
    # required_bins_control = calculate_required_bins(len(TwoDRebinnedEdgesX) - 1, len(TwoDRebinnedEdgesY) - 1, non_zero_points_y)
    
    # unwrapped_qcd_mjjall_vs_mjjj_control = unwrap_2d_into_1d(qcd_mjjall_vs_mjjj_control_rebinned, "unwrapped_mjjall_vs_mjjj_control", non_zero_points_y, required_bins_control)
    # QCDFile.WriteObject(unwrapped_qcd_mjjall_vs_mjjj_control, "unwrapped_mjjall_vs_mjjj_control")
    # unwrapped_ttbar_mjjall_vs_mjjj_control = unwrap_2d_into_1d(ttbar_mjjall_vs_mjjj_control_rebinned, "unwrapped_mjjall_vs_mjjj_control", non_zero_points_y, required_bins_control)
    # TTbarFile.WriteObject(unwrapped_ttbar_mjjall_vs_mjjj_control, "unwrapped_mjjall_vs_mjjj_control")
    
    # signal_mjjall_vs_mjjj_control_rebinned = rebinHisto(TwoDRebinnedModel, SignalFile.Get("mjjall_vs_mjjj_control"), "mjjall_vs_mjjj_control_rebinned")
    # SignalFile.WriteObject(signal_mjjall_vs_mjjj_control_rebinned, "mjjall_vs_mjjj_control_rebinned")
    # unwrapped_control_mjjall_vs_mjjj_control = unwrap_2d_into_1d(signal_mjjall_vs_mjjj_control_rebinned, "unwrapped_mjjall_vs_mjjj_control", non_zero_points_y, required_bins_control)
    # SignalFile.WriteObject(unwrapped_control_mjjall_vs_mjjj_control, "unwrapped_mjjall_vs_mjjj_control")
    # dummy_unwrapped_control = create_dummy_unwrapped(unwrapped_control_mjjall_vs_mjjj_control, "dummy_hist")
    # SignalFile.WriteObject(dummy_unwrapped_control, "unwrapped_dummy_control")
    
    # jet_ht_mjjall_vs_mjjj_control_rebinned = rebinHisto(TwoDRebinnedModel, JetHTFile.Get("mjjall_vs_mjjj_control"), "mjjall_vs_mjjj_control_rebinned")
    # JetHTFile.WriteObject(jet_ht_mjjall_vs_mjjj_control_rebinned, "mjjall_vs_mjjj_control_rebinned")
    # unwrapped_jet_ht_mjjall_vs_mjjj_control = unwrap_2d_into_1d(jet_ht_mjjall_vs_mjjj_control_rebinned, "unwrapped_mjjall_vs_mjjj_control", non_zero_points_y, required_bins_control)
    # JetHTFile.WriteObject(unwrapped_jet_ht_mjjall_vs_mjjj_control, "unwrapped_mjjall_vs_mjjj_control")

    
    
if __name__ == '__main__':
    for i in range(3):
        rebin_histograms(i)