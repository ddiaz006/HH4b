import numpy as np
from coffea.nanoevents.methods.nanoaod import JetArray, FatJetArray
from coffea.nanoevents.methods.base import NanoEventsArray
from .corrections import get_jetveto

# ak4 jet definition
def good_ak4jets(jets: JetArray, year: str, run: np.ndarray, isData: bool):
    # FIXME: check PuID WP and JetIDWP for Run3
    # PuID might only be needed for forward region (WIP)
    # JETID: https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID13p6TeV
    # 2 working points: tight and tightLepVeto
    goodjets = ( 
        (jets.isTight)
        # & ((jets.pt < 50) & (jets.puId >=6)) | (jets.pt >=50)
        & (abs(jets.eta) < 4.7)
    )
    if year=="2022" and isData:
        jet_veto = get_jetveto(jets, year, run)
        goodjets = goodjets & ~(jet_veto)

    return jets[goodjets]

# ak8 jet definition
def good_ak8jets(fatjets: FatJetArray):
    # add extra variables to FatJet collection
    fatjets["Txbb"] = fatjets.particleNetMD_Xbb / (
        fatjets.particleNetMD_QCD + fatjets.particleNetMD_Xbb
    )
    fatjets["Txjj"] = (fatjets.particleNetMD_Xbb + fatjets.particleNetMD_Xcc + fatjets.particleNetMD_Xqq) / (
        (fatjets.particleNetMD_Xbb + fatjets.particleNetMD_Xcc + fatjets.particleNetMD_Xqq + fatjets.particleNetMD_QCD)
    )
    return fatjets[
        (
            (abs(fatjets.eta) < 2.5) & (fatjets.isTight)
        )
    ]
