import ROOT as r
import json
import sys
import re
import os


def findEfficiency(inFile, wp):
    f = r.TFile.Open(inFile)
    efficiency1 = f.Get("j1_pNet").Integral(f.Get("j1_pNet").FindBin(wp), f.Get("j1_pNet").GetNbinsX()) / f.Get("j1_pNet").Integral()
    efficiency2 = f.Get("j2_pNet").Integral(f.Get("j2_pNet").FindBin(wp), f.Get("j2_pNet").GetNbinsX()) / f.Get("j2_pNet").Integral()
    efficiency3 = f.Get("j3_pNet").Integral(f.Get("j3_pNet").FindBin(wp), f.Get("j3_pNet").GetNbinsX()) / f.Get("j3_pNet").Integral()
    
    return efficiency1, efficiency2, efficiency3

if __name__ == '__main__':
    print(findEfficiency("/users/fbilandzija/H3PO/Analysis/background/scaled/QCD17.root", 0.9105))
    print(findEfficiency("/users/fbilandzija/H3PO/Analysis/background/scaled/TTbar17.root", 0.9105))
    
    
# (0.019576922472749298, 0.007147991482603713, 0.01158205584225806)
# (0.11518409845847107, 0.1349753207853279, 0.12551745457847419)
    