from ROOT import TFile, TH1F
prefix = 'AnalysisHistograms_V7/'
histdirname = 'MonoHFatJetSelection_JetAndLeptonVeto'
lumi = 2.23635*1000.

samples={
    ## data 
    'data_obs' : {
        'order' : 0,
        'files' : ['Merged_MET.root'],
        'xsec'      : [1.],
        'fillcolor' : 0,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "Data",
        'weight': [1.],
        'plot': True,
        },
    
    ## TT-Bar
    'TT' : {
        'order' : 0,
        'files' : ['Merged_TT_TuneCUETP8M1_13TeV-powheg-pythia8-runallAnalysis.root'],
        'xsec'      : [831.76],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "t#bar{t}",
        'weight': [1.],
        'plot': True,
        },
    
    ## Z ->nunu + Jets
    'znunujets' : {
        'order' : 0,
        'files' : ['Merged_ZJetsToNuNu_HT-100To200_13TeV-madgraph-runallAnalysis.root','Merged_ZJetsToNuNu_HT-200To400_13TeV-madgraph-runallAnalysis.root','Merged_ZJetsToNuNu_HT-400To600_13TeV-madgraph-runallAnalysis.root','Merged_ZJetsToNuNu_HT-600ToInf_13TeV-madgraph-runallAnalysis.root'],
        'xsec'      : [1.626*280.47, 1.617*78.36, 1.459*10.94, 1.391*4.203],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "t#bar{t}",
        'weight': [1.,1.,1.,1.],
        'plot': True,
        },

    ## W + Jets
    'wjets' : {
        'order' : 0,
        'files' : ['Merged_WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-runallAnalysis.root','Merged_WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-runallAnalysis.root','Merged_WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-runallAnalysis.root','Merged_WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-runallAnalysis.root','Merged_WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-runallAnalysis.root','Merged_WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-runallAnalysis.root','Merged_WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-runallAnalysis.root'],
        'xsec'      : [1.459*1347., 1.434*360., 1.532*48.9, 1.004*12.8, 1.004*5.26, 1.004*1.33, 1.004*0.03089],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "t#bar{t}",
        'weight': [1.,1.,1., 1.,1.,1., 1.],
        'plot': True,
        },


    ## Diboson
    'VV' : {
        'order' : 0,
        'files' : ['Merged_WW_TuneCUETP8M1_13TeV-pythia8-runallAnalysis.root','Merged_WZ_TuneCUETP8M1_13TeV-pythia8-runallAnalysis.root','Merged_ZZ_TuneCUETP8M1_13TeV-pythia8-runallAnalysis.root'],
        'xsec'      : [118.7, 66.1, 15.4],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "t#bar{t}",
        'weight': [1.,1.,1.],
        'plot': True,
        },


    ## ZH
    'ZH' : {
        'order' : 0,
        'files' : ['Merged_ZH_HToBB_ZToNuNu_M120_13TeV_amcatnloFXFX_madspin_pythia8-runallAnalysis.root'],
        'xsec'      : [0.8696*0.577*0.2],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "ZH",
        'weight': [1.],
        'plot': True,
        },

    ## Single Top
    'ST' : {
        'order' : 0,
        'files' : ['Merged_ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1-runallAnalysis.root','Merged_ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1-runallAnalysis.root','Merged_ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1-runallAnalysis.root','Merged_ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1-runallAnalysis.root','Merged_ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1-runallAnalysis.root'],
        'xsec'      : [3.36, 26.38, 44.33, 35.6, 35.6],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "Single Top",
        'weight': [1.,1.,1.,1.,1.],
        'plot': True,
        },

    ## Sigmal
    'signal600' : {
        'order' : 0,
        'files' : ['Merged_MonoHToBBarMZp-600GeV_MA0-300GeV-runallAnalysis.root'],
        'xsec'      : [0.026],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "",
        'weight': [1.],
        'plot': True,
        },

    ## Sigmal
    'signal800' : {
        'order' : 0,
        'files' : ['Merged_MonoHToBBarMZp-800GeV_MA0-300GeV-runallAnalysis.root'],
        'xsec'      : [0.0288],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "",
        'weight': [1.],
        'plot': True,
        },

    ## Sigmal
    'signal1000' : {
        'order' : 0,
        'files' : ['Merged_MonoHToBBarMZp-1000GeV_MA0-300GeV-runallAnalysis.root'],
        'xsec'      : [0.02337],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "",
        'weight': [1.],
        'plot': True,
        },

    ## Sigmal
    'signal1200' : {
        'order' : 0,
        'files' : ['Merged_MonoHToBBarMZp-1200GeV_MA0-300GeV-runallAnalysis.root'],
        'xsec'      : [0.01832],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "",
        'weight': [1.],
        'plot': True,
        },

    ## Sigmal
    'signal1400' : {
        'order' : 0,
        'files' : ['Merged_MonoHToBBarMZp-1400GeV_MA0-300GeV-runallAnalysis.root'],
        'xsec'      : [0.01359],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "",
        'weight': [1.],
        'plot': True,
        },

    ## Sigmal
    'signal1700' : {
        'order' : 0,
        'files' : ['Merged_MonoHToBBarMZp-1700GeV_MA0-300GeV-runallAnalysis.root'],
        'xsec'      : [0.00871],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "",
        'weight': [1.],
        'plot': True,
        },

    ## Sigmal
    'signal2000' : {
        'order' : 0,
        'files' : ['Merged_MonoHToBBarMZp-2000GeV_MA0-300GeV-runallAnalysis.root'],
        'xsec'      : [0.00561],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "",
        'weight': [1.],
        'plot': True,
        },

    ## Sigmal
    'signal2500' : {
        'order' : 0,
        'files' : ['Merged_MonoHToBBarMZp-2500GeV_MA0-300GeV-runallAnalysis.root'],
        'xsec'      : [0.00280],
        'fillcolor' : 2,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "",
        'weight': [1.],
        'plot': True,
        },

    }


def FindIntegral(filename):
    filename = prefix + '/' + filename
    infile_ = TFile(filename,'READ')
    h_mJ = TH1F()
    histname = histdirname+'/h_MET0'
    h_mJ = infile_.Get(histname)
    h_total = infile_.Get('h_total')
    return [h_mJ.Integral(),h_total.Integral()]

    
##############################################################
## Loop over all files and fill weights and cross-sections
##############################################################
def setweights():
    for isample in samples:
        ixsec=0
        for ifile in samples[isample]['files']:
            #print ifile 
            integral_ =  FindIntegral(ifile)
            weight = samples[isample]['xsec'][ixsec] * lumi  / integral_[1]
            #print "weight = ", weight
            samples[isample]['weight'][ixsec] = weight
            ixsec=ixsec+1
    return 0




if __name__ == "__main__":
    print ("running the models of Util.py directly to test them. ")
    setweights()
    
else :
    print ("Utils.py is being imported as a module......")
        
