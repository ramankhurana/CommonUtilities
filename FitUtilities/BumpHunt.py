### 
###
# Created By : Raman Khurana
# Date       : 03:March:2016
# Time       : 22:20:30 
###
###
## $ROOTSYS/tutorials/roofit/rf109_chi2residpull.C

## references: https://github.com/wangmengmeng/ExoDiBosonResonances/blob/bf5d2e79f59ad25c7a11e7f97552e2bf6a283428/EDBRCommon/test/fits_dijetStyle/R2JJFitter.cc#L1265
## references: https://twiki.cern.ch/twiki/bin/view/CMS/DensityEstimation

## import user defined modules
#from Utils import *
import Utils

## this imports basics
from array import array
import math
from ROOT import gROOT, gSystem, gStyle, gRandom
from ROOT import TFile, TChain, TTree, TCut, TH1F, TH2F, THStack, TGraph, TGaxis, TF1, TMath
from ROOT import TStyle, TCanvas, TPad, TLegend, TLatex, TText

#from ROOT import TFile, TTree, TH1F, TH2F, TCanvas, TColor, TAttLine, TAttFill 
from ROOT import RooRealVar, RooArgSet, RooDataSet, RooHistPdf
from ROOT import RooFit, RooRealVar, RooDataHist, RooDataSet, RooAbsData, RooAbsReal, RooAbsPdf, RooPlot, RooBinning, RooCategory, RooSimultaneous, RooArgList, RooArgSet, RooWorkspace, RooMsgService, RooArgusBG
from ROOT import RooFormulaVar, RooGenericPdf, RooGaussian, RooExponential, RooPolynomial, RooChebychev, RooBreitWigner, RooCBShape, RooExtendPdf, RooAddPdf, RooProdPdf, RooNumConvPdf, RooFFTConvPdf

from ROOT import RooArgusBG, RooBCPEffDecay, RooBMixDecay, RooBifurGauss, RooBreitWigner, RooCBShape, RooChebychev, RooDecay,  RooDstD0BG
from ROOT import RooExponential, RooKeysPdf, Roo2DKeysPdf, RooPolynomial, RooVoigtian, RooGenericPdf, RooHist
import sys, optparse
import os
###################################
## set up running mode of the code. 
###################################
usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)
## data will be true if -d is passed and will be false if -m is passed
parser.add_option("-d", "--data", action="store_true",  dest="data")
parser.add_option("-m", "--mc", action="store_false",  dest="data")
parser.add_option("-s", "--signal", action="store_true",  dest="signal")
parser.add_option("-b", "--sidebands", action="store_true",  dest="sidebands")
parser.add_option("-t", "--fullrange", action="store_true", default=False, dest="fullrange")

(options, args) = parser.parse_args()

print 'options = ',[options.data]



########################################
## User's defined PDF
########################################

gSystem.Load("PDFs/HWWLVJRooPdfs_cxx.so")
gSystem.Load("PDFs/PdfDiagonalizer_cc.so")
from ROOT import RooErfExpPdf
from ROOT import *


#########################################
#
# Set Weights for each sample
#
#########################################

#Utils.setweights()
debug_=False



## Define the mass variable as RooRealVar
J_Mass       = RooRealVar ('J_Mass' ,'M_{Jet}[GeV]' ,  580., 1200.)
#J_Mass.setBins(28)
## set range and bins
J_Mass.setRange('Full',580., 1200.)



##########################################
# 
#   #####    ####    ####  #######
#   #   #   #    #  #    #    #
#   #   #   #    #  #    #    #
#   ####    #    #  #    #    #
#   #  #    #    #  #    #    #
#   #   #    ####    ####     #
#
##########################################
## Accessing the RootFile

filedata = TFile('RootFilesXbb/Xbb.root', 'READ')
MPruned_Merged = filedata.Get('mass')
hist_integral = MPruned_Merged.Integral()
print MPruned_Merged.Integral()
mean_vaue= MPruned_Merged.GetMean()
rms_value= MPruned_Merged.GetRMS()
print MPruned_Merged.GetNbinsX()
MPruned_hist = RooDataHist('MPruned_hist','MPruned_hist',RooArgList(J_Mass),MPruned_Merged)



##########################################
#    
#    #####   ####    #####
#    #    #  #   #   #
#    #    #  #   #   #
#    ####    #   #   #####
#    #       #   #   #
#    #       ####    #
#
###########################################

## signal
mean   = RooRealVar ('mean','mean',85.,0,250)
sigma  = RooRealVar ('sigma','sigma',100.0,0,250)
gauss  = RooGaussian('gauss','gaussian', J_Mass, mean, sigma)


## background model
## exponential 
slopeQCD  = RooRealVar("slopeQCD", "slopeQCD", -0.1, -20., 20.)
expQCD    = RooExponential("expQCD", "exponential PDF", J_Mass, slopeQCD)

##p2mod     = 4.99989      +/-  3.9569    (limited)
##p3mod     = 11.9997      +/-  0.529866  (limited)
##p4mod     = 2.02636      +/-  0.360492  (limited)
##p5mod     = 0.220746     +/-  0.0842075 (limited)

## dijet mass function
f_var     = RooFormulaVar('f_var','f_var','@0/13000.',RooArgList(J_Mass))

p1mod = RooRealVar('p1mod','p1mod', 0.,4000)
p2mod = RooRealVar('p2mod','p2mod',-2000.,2000.)
p3mod = RooRealVar('p3mod','p3mod',-1000,1000.)
p4mod = RooRealVar('p4mod','p4mod',-100.,100.)
p5mod = RooRealVar('p5mod','p5mod',-200.,200.)
p6mod = RooRealVar('p6mod','p6mod',-10,10.)


diJetMass   = RooGenericPdf('diJetMass'  , "pow(1-@0,@2)/pow(@0, @1+@3*log(@0))", RooArgList(f_var, p4mod, p2mod,p3mod))
diJetMass_2 = RooGenericPdf('diJetMass_2', "1.0/pow(@0,@1)", RooArgList(f_var,p3mod))
diJetMass_3 = RooGenericPdf('diJetMass_3', "pow(1-@0,@1)/pow(@0,@2)",RooArgList(f_var,p2mod,p3mod))
diJetMass_4 = RooGenericPdf('diJetMass_4', "pow(1-@0,@1)/pow(@0, @2+@3*log(@0))", RooArgList(f_var, p2mod,p3mod,p4mod))
diJetMass_5 = RooGenericPdf('diJetMass_5', "pow(1-@0,@1)/pow(@0, @2+@3*log(@0)+@4*pow(log(@0),2))", RooArgList(J_Mass, p2mod,p3mod,p4mod,p5mod))

##polynomial of order 5
#diJetMass_5 = RooGenericPdf('diJetMass_5', "@1+@2*pow(@0,1)+@3*pow(@0,2)+@4*pow(@0,3)+@5*pow(@0,4)+@6*pow(@0,5)",RooArgList(J_Mass,p1mod,p2mod,p3mod,p4mod,p5mod,p6mod))
#diJetMass_5 = RooGenericPdf('diJetMass_5', "@1*pow(@0,1)+@2*pow(@0,2)+@3*pow(@0,3)+@4*pow(@0,4)+@5*pow(@0,5)",RooArgList(J_Mass,p2mod,p3mod,p4mod,p5mod,p6mod))
#x= RooRealVar("x","x", 500,1500)
#x.setRange(520,1500)
#diJetMass_5 = RooBernstein ("diJetMass_5","diJetMass_5",x,RooArgList(p1mod,p2mod,p3mod,p4mod,p5mod,p6mod))
#diJetMass_2 = RooGenericPdf('diJetMass_2', "1.0/pow(@0,@2)", RooArgList(x,p3mod))
#diJetMass_3 = RooGenericPdf('diJetMass_3', "pow(1-@0,@2)/pow(@0,@3)",RooArgList(x,p1mod,p2mod,p3mod))
#diJetMass_4 = RooGenericPdf('diJetMass_4', "pow(1-@0,@2)/pow(@0, @3+@4*log(@0))", RooArgList(x, p1mod, p2mod,p3mod,p4mod))
#diJetMass_5 = RooGenericPdf('diJetMass_5', "pow(1-@0,@2)/pow(@0, @3+@4*log(@0)+@5*pow(log(@0),2))", RooArgList(x, p1mod, p2mod,p3mod,p4mod,p5mod))
#diJetMass_4 = RooGenericPdf('diJetMass_4', "pow(1-@0, @2)/pow(@0, @1+@3*log(@0))", RooArgList(x, p1mod, p2mod,p3mod))

## Erf x Exp 
constQCD  = RooRealVar('constQCD' ,'constQCD' , -0.02,  -1.,    0.)
offsetQCD = RooRealVar('offsetQCD','offsetQCD', 70.,     -0.,  200.)
widthQCD  = RooRealVar('widthQCD' ,'widthQCD' , 30.,      0.1,  100.)
ErfExpQCD = RooErfExpPdf("ErfExpQCD", "error function for Z+jets mass", J_Mass, constQCD, offsetQCD, widthQCD)


##########################################
#
#   #####  #####    #######    ####
#   #      #    #   #     #   #
#   #      #    #   #     #  #
#   #####  ####     #######  #
#   #      #  #     #     #  #
#   #      #   #    #     #   #
#   #      #    #   #     #    ####
##########################################


## fraction parameters
## for signal
signalfrac = RooRealVar('signalfrac','signalfrac',0.01,0,0.1)

##########################################
#    
#    #####   ####    #####       ####    #####   
#    #    #  #   #   #          #    #   #    #  
#    #    #  #   #   #          #    #   #    #  
#    #####   #   #   #####      #    #   ####    
#    #       #   #   #          #    #   #       
#    #       ####    #           ####    #       
#
##########################################

model = RooAddPdf('model','model',RooArgList(expQCD,gauss), RooArgList(signalfrac))


####################################################################################################################
## weighted and summed over all samples histograms for a given physics process. 
####################################################################################################################
def MakeRooDataHist(phys_process, fullrange_=False):
    MPruned_Merged.Scale(0.0)
    iweight = 0
    for irootfile in Utils.samples[phys_process]['files']:
        
        file01 = TFile('AnalysisHistograms_V7/'+irootfile, 'READ')
        #file01 = TFile(irootfile, 'READ')
        
        MPruned_ttbar_sb  = file01.Get('histfacFatJet_ZLight/h_Mjj0')
        MPruned_ttbar_sig = file01.Get('MonoHFatJetSelection_JetAndLeptonVeto/h_Mjj0')
        
        if debug_ :
            print "before ",MPruned_ttbar_sb.Integral()
            print "before ",MPruned_ttbar_sig.Integral()
        
        if phys_process != 'data_obs' :
            MPruned_ttbar_sb.Scale(Utils.samples[phys_process]['weight'][iweight])
            MPruned_ttbar_sig.Scale(Utils.samples[phys_process]['weight'][iweight])
        
        if debug_ :
            print "weight = ", Utils.samples[phys_process]['weight'][iweight]
            print "after ",MPruned_ttbar_sb.Integral()
            print "after ",MPruned_ttbar_sig.Integral()
        
        
        MPruned_Merged.Add(MPruned_ttbar_sb)
        if fullrange_ | options.fullrange :
            MPruned_Merged.Add(MPruned_ttbar_sig)
        ## convert Histogram to RooDataHist
        MPruned_ttbar_hist = RooDataHist('MPruned_ttbar_hist','MPruned_ttbar_hist',RooArgList(J_Mass),MPruned_Merged)
        iweight = iweight +1 
    print "final intgral = ",MPruned_Merged.Integral()
    return MPruned_ttbar_hist

############################################################
## background RooDataHist taken from input Rootfiles. 
## to fix the normalisation and pdf of TT and VV and ZH
############################################################
calllikethis='''h_tt_FR    = MakeRooDataHist('TT',True) ## tripple gaussian '''


def FitOnePdf(dataset, process_name):
    ## set canvas and frame
    c = TCanvas()
    frame = J_Mass.frame()
    pdf_ = pdfDict[process_name]
    pdf_.fitTo(dataset,RooFit.Range('R1'), RooFit.Strategy(2),RooFit.Minimizer('Minuit2'))
    dataset.plotOn(frame)
    pdf_.plotOn(frame)
    frame.Draw()
    c.SaveAs('Plots/'+process_name+'.png')
    return 0


########################################
## Fix PDF For TTBar + Single Top
########################################    
calllikethis1='''FitOnePdf(h_Top_FR, 'tt')'''

#h_Top_FR.sum(False)
sigma_ = math.sqrt(hist_integral)
up_ = hist_integral + 5 * sigma_
down_ = hist_integral - 5* sigma_

nQCD  = RooRealVar("nQCD", "QCD normalization", hist_integral,  down_, up_  )#500,  0., 1200)
ndijet  = RooRealVar("ndijet", "dijet normalization",  4000, 0.0, 10000000)

#######################################
## Define Background Model
#######################################


diJetMass_ext = RooExtendPdf('diJetMass_ext','extended pdf for diJetMass',diJetMass, ndijet)
diJetMass_ext_2 = RooExtendPdf('diJetMass_ext_2','extended pdf for diJetMass_2',diJetMass_2, ndijet)
diJetMass_ext_3 = RooExtendPdf('diJetMass_ext_3','extended pdf for diJetMass_3',diJetMass_3, ndijet)
diJetMass_ext_4 = RooExtendPdf('diJetMass_ext_4','extended pdf for diJetMass_4',diJetMass_4, ndijet)
diJetMass_ext_5 = RooExtendPdf('diJetMass_ext_5','extended pdf for diJetMass_5',diJetMass_5, ndijet)
exp_ext     = RooExtendPdf('exp_ext',  'extended p.d.f for QCD', expQCD,  nQCD)

# add pdf to make big extended pdf.
#bkgModel = RooAddPdf("bkgModel","bkgModel",RooArgList( VJets_ext, TT_ext, VV_ext, ZH_ext), RooArgList(nVJets, nTop, nVV, nZH))

'''
models={'F1' : exp_ext,
        'F2' : diJetMass_ext_2,
        'F3' : diJetMass_ext_3,
        'F4' : diJetMass_ext_4,
        'F5' : diJetMass_5
#        'F5' : diJetMass_ext_5
}
'''
models={'F2' : diJetMass_2,
        'F3' : diJetMass_3,
        'F4' : diJetMass_4,
        'F5' : diJetMass_5
#        'F5' : diJetMass_ext_5
}
##########################################
#
#    ######  #  #########
#    #       #      #
#    #       #      #
#    #####   #      #
#    #       #      #
#    #       #      #
#  
##########################################
## fit the model

def fitAndSaveEE(h_st, imageName):
    ## set canvas and frame
    c = TCanvas()
    
    frame = J_Mass.frame()
    #fitres = diJetMass_ext.fitTo(h_st,RooFit.Range('Full'), RooFit.Strategy(2),RooFit.Minimizer('Minuit2'),RooFit.Save(),RooFit.Extended(True))
    #h_st.plotOn(frame)
    #diJetMass_ext.plotOn(frame,RooFit.VisualizeError(fitres,1,kFALSE),RooFit.FillColor(3), RooFit.FillStyle(3001)) 
    #diJetMass_ext.plotOn(frame)
    
    #fitres = exp_ext.fitTo(h_st,RooFit.Range('Full'), RooFit.Strategy(2),RooFit.Minimizer('Minuit2'),RooFit.Save(),RooFit.Extended(True))
    #h_st.plotOn(frame)
    #exp_ext.plotOn(frame,RooFit.VisualizeError(fitres,1,kFALSE),RooFit.FillColor(3), RooFit.FillStyle(3001)) 
    #exp_ext.plotOn(frame)


   ##background model taken from dictionary
    bkgModel=models[imageName]
    
    #fitres = bkgModel.fitTo(h_st,RooFit.Range('Full'), RooFit.Strategy(2),RooFit.Minimizer('Minuit2'),RooFit.Save(),RooFit.Extended(True)) 
    #fitres = bkgModel.fitTo(h_st,RooFit.Range('Full'), RooFit.Strategy(2),RooFit.Minimizer('Minuit2'),RooFit.Save()) 
    currentlist = RooLinkedList()
    fitres = bkgModel.chi2FitTo(h_st, currentlist)
    h_st.plotOn(frame)
    #bkgModel.plotOn(frame,RooFit.VisualizeError(fitres,1,kFALSE),RooFit.FillColor(3), RooFit.FillStyle(3001)) 
    bkgModel.plotOn(frame)
    
    commented='''
    ############ After fitting fix the pdf
    constWJets.setConstant(True)
    nVJets.setConstant(True)
    offsetWJets.setConstant(True)
    widthWJets.setConstant(True)
    ########### Integrate Over PDF to get SR fractions.
    J_MassArgSet = RooArgSet(J_Mass)
    VVSR     =  VV_ext.createIntegral(J_MassArgSet, RooFit.NormSet(J_MassArgSet), RooFit.Range('signal'))
    ZHSR     =  ZH_ext.createIntegral(J_MassArgSet, RooFit.NormSet(J_MassArgSet), RooFit.Range('signal'))
    TTSR     =  TT_ext.createIntegral(J_MassArgSet, RooFit.NormSet(J_MassArgSet), RooFit.Range('signal'))
    VJetsSR  =  VJets_ext.createIntegral(J_MassArgSet, RooFit.NormSet(J_MassArgSet), RooFit.Range('signal'))
    
    SRyield = RooFormulaVar("SRyield", "extrapolation to SR", "@0*@1 + @2*@3 + @4*@5 + @6*@7", RooArgList(VVSR, nVV, ZHSR, nZH, TTSR, nTop, VJetsSR, nVJets))
    print 'backgorund total = ',SRyield.getVal()

    print "fractions ",[VVSR,ZHSR,TTSR,VJetsSR]
    comptt = RooArgSet(TT_ext)
    compvv = RooArgSet(VV_ext)
    compzh = RooArgSet(ZH_ext)
    compVJets = RooArgSet(VJets_ext)
    '''
    import ROOT
    chi2value = frame.chiSquare()
    
    #chi2=TString('#chi^{2}/ndof = '+str(chi2value))
    txt = ROOT.TLatex(0.7,0.8 ,"#chi^{2}/ndof = %.2f" %chi2value)    
    txt.SetNDC()
    #txt = TText(800,130,chi2) ;
    txt.SetTextSize(0.04) ;
    txt.SetTextColor(kRed) ;
    frame.addObject(txt) 
    print frame.chiSquare()
    frame.Draw()

    plotname='Plots/'+imageName+'.png'
    c.SaveAs(plotname)
    os.system('mv '+plotname+' /afs/hep.wisc.edu/home/khurana/public_html/Analysis/Xbb/')

    residualHist = frame.residHist()
    c1 = TCanvas()
    residualHist.Draw()
    residualplotname = 'Plots/residualHist_'+imageName+'.png' 
    c1.SaveAs(residualplotname)
    os.system('mv '+residualplotname+' /afs/hep.wisc.edu/home/khurana/public_html/Analysis/Xbb/Plots/')

    a=ROOT.Double(0.0)
    b=ROOT.Double(0.0)
    
    SumResidual =0
    SumSquareResidual = 0
    for x in xrange(0,residualHist.GetN()):
        residualHist.GetPoint(x,a,b)
        #print 'point = ',[a,b]
        SumResidual = SumResidual + b
        #print 'SumResidual = ',SumResidual
        SumSquareResidual = SumSquareResidual + b*b
        #print 'SumSquareResidual = ',SumSquareResidual
    return [fitres,SumSquareResidual]

## fit the data
## fit MC background with data
#[fitRes1,SumSquareResidual1] = fitAndSaveEE(MPruned_hist,'F1')
[fitRes2,SumSquareResidual2] = fitAndSaveEE(MPruned_hist,'F2')
[fitRes3,SumSquareResidual3] = fitAndSaveEE(MPruned_hist,'F3')
[fitRes4,SumSquareResidual4] = fitAndSaveEE(MPruned_hist,'F4')
#[fitRes5,SumSquareResidual5] = fitAndSaveEE(MPruned_hist,'F5')
[fitRes5,SumSquareResidual5] = fitAndSaveEE(MPruned_hist,'F5')

## to print number of bins
#print 'number of bins ',reshist1.GetN()
#print 'SumSquareResidual1 = ',SumSquareResidual1
print 'SumSquareResidual2 = ',SumSquareResidual2
print 'SumSquareResidual3 = ',SumSquareResidual3
print 'SumSquareResidual4 = ',SumSquareResidual4
print 'SumSquareResidual5 = ',SumSquareResidual5


# Ftest calculation


def GetF21(rss1, rss2, n1, n2):
    Nbin = 28
    ndof_parameter = Nbin-n2
    f21 = (rss1-rss2)/(n2-n1)/(rss2/(ndof_parameter))
    CLF21 = 1.- (TMath.FDistI(f21,(n2-n1),ndof_parameter))
    return [f21,CLF21]

'''

[F21,good_CL21] = GetF21(SumSquareResidual1,SumSquareResidual2,2,3)
[F32,good_CL32] = GetF21(SumSquareResidual2,SumSquareResidual3,3,4)
[F43,good_CL43] = GetF21(SumSquareResidual3,SumSquareResidual4,4,5)
[F54,good_CL54] = GetF21(SumSquareResidual4,SumSquareResidual5,5,6)

print 'F21 = ',F21     
print 'F32 = ',F32    
print 'F43 = ',F43    
print 'F54 = ',F54    
    
print 'good_CL21 = ', good_CL21
print 'good_CL32 = ', good_CL32
print 'good_CL43 = ', good_CL43
print 'good_CL54 = ', good_CL54

'''
# another way to acess y value
#YValues=reshist1.GetY()
#print 'Y Value 1', YValues[0]

#print 'bin 1 ',reshist1.weight()
#print 'numEntries() = ',reshist1.numEntries()


'''
fitRes1.Print('v')
fitRes2.Print('v')
fitRes3.Print('v')
fitRes4.Print('v')

## For F test 
## fit parameters can be accessed using follaoing syntax
## You need to know the name of the parameters. 
## Otherwise simply do 
## fitRes1.Print('v')
## and this will print the information you need to know the parameters. 


print 'slopeQCD = ',fitRes1.floatParsFinal().find("slopeQCD").getVal()
par1_fitresult = fitRes1.floatParsFinal().find('slopeQCD')
print 'value = ',par1_fitresult.getVal()
print 'error = ',par1_fitresult.getError()

print MPruned_Merged.Integral()
nbins = MPruned_Merged.GetNbinsX()
print MPruned_Merged.GetBinContent(1)
poly_2_0 = fitRes2.floatParsFinal().find('ndijet')
poly_2_1 = fitRes2.floatParsFinal().find('p3mod')

poly_3_0 = fitRes3.floatParsFinal().find('ndijet')
poly_3_1 = fitRes3.floatParsFinal().find('p2mod')
poly_3_2 = fitRes3.floatParsFinal().find('p3mod')

poly_4_0 = fitRes4.floatParsFinal().find('ndijet')
poly_4_1 = fitRes4.floatParsFinal().find('p2mod')
poly_4_2 = fitRes4.floatParsFinal().find('p3mod')
poly_4_3 = fitRes4.floatParsFinal().find('p4mod')

poly_4_0 = fitRes5.floatParsFinal().find('ndijet')
poly_4_1 = fitRes5.floatParsFinal().find('p2mod')
poly_4_2 = fitRes5.floatParsFinal().find('p3mod')
poly_4_3 = fitRes5.floatParsFinal().find('p4mod')
poly_4_4 = fitRes5.floatParsFinal().find('p5mod')




f2 = TF1("f2","[0]/(x**[1])");                                                                                            
f2.SetParameters(poly_2_0.getVal(),poly_2_1.getVal());

print f2.Eval(500./13000.)


#diJetMass_2 = RooGenericPdf('diJetMass_2', "1.0/pow(@0,@1)", RooArgList(x,p3mod))
#diJetMass_3 = RooGenericPdf('diJetMass_3', "pow(1-@0,@1)/pow(@0,@2)",RooArgList(x,p2mod,p3mod))
#diJetMass_4 = RooGenericPdf('diJetMass_4', "pow(1-@0,@1)/pow(@0, @2+@3*log(@0))", RooArgList(x, p2mod,p3mod,p4mod))
#diJetMass_5 = RooGenericPdf('diJetMass_5', "pow(1-@0,@1)/pow(@0, @2+@3*log(@0)+@4*pow(log(@0),2))", RooArgList(x, p2mod,p3mod,p4mod,p5mod))
#
#for( int i = 1; i <nbins ; i++){



#}




'''


## One can access RooFitResults from this rootfile and perform the F-test.
## With Some more information this rootfile can be used to perform the bias study also. 
## somehow need to write the pdf into this rootfile which is possible by workspace but this doesn't seem to work for now. 
fout = TFile('FitResults.root','RECREATE')
fout.cd()
#MPruned_hist.Write()
#fitRes1.Write()
#reshist1.Write()
#fitRes2.Write()
#fitRes3.Write()
#fitRes4.Write()
#fitRes5.Write()
fout.Close()

## I think most of the things needed for F-Test are now done. 
## So Happy Testing :) 
