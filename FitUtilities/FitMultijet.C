#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooExtendPdf.h"
#include "RooFitResult.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "TLegend.h"
using namespace RooFit ;
void FitMultijet(){
  TFile *f1 = new TFile("Full_discrepancy_fit_withoutdeltaphicut.root","read");
  //TFile *f1 = new TFile("Full_discrepanc_greater02.root","read");
  f1->cd();
  TString analysistype  = "0ptag2pjet_0ptv";
  TString region =  "SRVBS" ;
  TString histname = "SmallestDeltaPhismallJet_MET";
  TString totalname = analysistype+"_"+region+"_"+histname;
  
  TH1F *h1_data = (TH1F*) f1->Get("data_"+totalname);
  TH1F *h1_ttbar = (TH1F*) f1->Get("ttbar_"  +totalname);
  TH1F *h1_W = (TH1F*) f1->Get("W_"      +totalname);
  TH1F *h1_Z = (TH1F*) f1->Get("Z_"      +totalname);
  TH1F *h1_stops = (TH1F*) f1->Get("stops_"  +totalname);
  TH1F *h1_stopt = (TH1F*) f1->Get("stopt_"  +totalname);
  TH1F *h1_stopWt = (TH1F*) f1->Get("stopWt_" +totalname);
  TH1F *h1_WW = (TH1F*) f1->Get("WW_"     +totalname);
  TH1F *h1_WZ = (TH1F*) f1->Get("WZ_"     +totalname);
  TH1F *h1_ZZ = (TH1F*) f1->Get("ZZ_"     +totalname);
  std::cout << h1_data->Integral()<< std::endl;

  
  TH1F *h_other = (TH1F*) h1_WZ->Clone();
  h_other->Add(h1_WW );
  h_other->Add(h1_ZZ );
  h_other->Add(h1_stopt);
  h_other->Add(h1_stopWt);
  h_other->Add(h1_stops);


  std::cout<<" tt "<< h1_ttbar->Integral()
	   <<" W "<< h1_W->Integral()
           <<" Z "<< h1_Z->Integral()
	   <<" other "<< h_other->Integral()
	   <<std::endl;

  

  
  RooRealVar x("x", "x", 0., 3.2);
  RooDataHist* temp_data = new RooDataHist("temp_data", "temp_data", RooArgList(x), h1_data);
  RooDataHist* temp_tt = new RooDataHist("temp_tt", "temp_tt", RooArgList(x), h1_ttbar);
  RooDataHist* temp_W = new RooDataHist("temp_W", "temp_W", RooArgList(x), h1_W);
  RooDataHist* temp_Z = new RooDataHist("temp_Z", "temp_Z", RooArgList(x), h1_Z);
  RooDataHist* temp_others = new RooDataHist("temp_others", "temp_others", RooArgList(x), h_other);
  
  RooHistPdf pdf_tt("pdftt", "pdf_tt", RooArgSet(x), *temp_tt);
  RooHistPdf pdf_W("pdf_W", "pdf_W", RooArgSet(x), *temp_W);
  RooHistPdf pdf_Z("pdf_Z", "pdf_Z", RooArgSet(x), *temp_Z);
  RooHistPdf pdf_others("pdf_others", "pdf_others", RooArgSet(x), *temp_others);


  RooRealVar coeff_tt("coeff_tt", "coeffModel", 16352, 15000, 20000);
  RooRealVar coeff_W("coeff_W", "coeffModel", 27000, 24000, 33000);
  RooRealVar coeff_Z("coeff_Z", "coeffModel", 28000, 20000, 30000);
  RooRealVar coeff_other("coeff_other", "coeffModel", 3869.71, 3869.71, 3869.71);
  RooRealVar coeff_qcd("coeff_qcd", "coeffModel", 44000, 25000, 75000 );
  // tt 16352.3 W 27946.7 Z 28301.6 other 3869.71
  
  RooRealVar lambda("lambda", "slope", -2., -10., 10.);
  RooExponential expo("expo", "exponential PDF", x, lambda);
  

  RooRealVar a0("a0","a0",1) ;
  RooRealVar a1("a1","a1",0,-1,1) ;
  RooRealVar a2("a2","a2",1,0,10) ;
  RooPolynomial p2("p2","p2",x,RooArgList(a0,a1,a2),0);



  
  x.setRange("signalRange",0.,3.2) ;
  x.setRange("expoRange",0.,0.5) ;
  RooExtendPdf ett("ett","extended tt p.d.f",pdf_tt,coeff_tt,"signalRange") ;
  RooExtendPdf eW("eW","extended W p.d.f",pdf_W,coeff_W,"signalRange") ;
  RooExtendPdf eZ("eZ","extended Z p.d.f",pdf_Z,coeff_Z,"signalRange") ;
  RooExtendPdf eothers("eothers","extended other p.d.f",pdf_others,coeff_other,"signalRange") ;
  RooExtendPdf eexpo("eexpo", "extended exp pdf", expo, coeff_qcd, "expoRange");
  
  RooAddPdf sumModel("sumModel", "coeffModel*pdf_tt + pdf_W + pdf_Z + pdf_others ", RooArgList(ett, eW, eZ, eothers, eexpo));
  //RooAddPdf sumModel("sumModel", "coeffModel*pdf_tt + pdf_W + pdf_Z + pdf_others ", RooArgList(pdf_tt, pdf_W, pdf_Z, pdf_others), RooArgList(coeffModel));
  
  // sumModel.fitTo(*temp_data, RooFit::Extended(kTRUE), RooFit::Minos(true));

  RooFitResult* r = sumModel.fitTo(*temp_data, RooFit::Extended(kTRUE), Save());
  r->Print("v") ;
  //RooRealVar* par1_fitresult = (RooRealVar*) r->floatParsFinal()->find("coeff_tt");
  RooRealVar* par1_fitresult = (RooRealVar*)r->floatParsFinal().find("coeff_tt");
  std::cout<< par1_fitresult->getValV()<<std::endl;
  //Bins(30)
  RooPlot* frame3 = x.frame(Name("xframe"),Title("Filled Curve / Blue Histo")) ;
  temp_data->plotOn(frame3,MarkerColor(kBlue),LineColor(kBlue)) ;
  sumModel.plotOn(frame3,Components(expo),LineStyle(kDashed),LineWidth(1));
  
  //  sumModel.plotOn(frame3,Components("ett,eW,eZ,eothers,eexpo"),DrawOption("F"),FillColor(kPink));
  sumModel.plotOn(frame3,Name("Fit_"),Components("ett,eW,eZ,eothers,eexpo"),DrawOption("L"),LineColor(kPink));
  //  sumModel.plotOn(frame3,Name("Fit"),Components(eexpo),DrawOption("F"),FillColor(kPink));
  sumModel.plotOn(frame3,Name("VVstop_"),Components("ett,eW,eZ,eothers"),DrawOption("F"),FillColor(kGray),LineColor(kGray));
  sumModel.plotOn(frame3,Name("Zjets_"),Components("ett,eW,eZ"),DrawOption("F"),FillColor(kBlue-4),LineColor(kBlue-4));
  sumModel.plotOn(frame3,Name("Wjets_"),Components("ett,eW"),DrawOption("F"),FillColor(kGreen+3),LineColor(kGreen+3));
  sumModel.plotOn(frame3,Name("ttbar_"),Components("ett"),DrawOption("F"),FillColor(kOrange),LineColor(kOrange));
  temp_data->plotOn(frame3,Name("Data_"),MarkerColor(kBlack),LineColor(kBlack)) ;
  sumModel.plotOn(frame3,Name("Multijet_"),Components(eexpo),LineColor(kBlue),LineStyle(kDashed),LineWidth(3));



  


  RooAbsReal* fracInt = eexpo.createIntegral(x,"signalRange");
  cout << fracInt->getVal() << endl;


  //.plotOn(frame3,DrawOption("F"),FillColor(kOrange),MoveToBack()) ;
  TCanvas* c = new TCanvas("rf107_plotstyles","rf107_plotstyles",800,800) ;

  c->cd() ; gPad->SetLeftMargin(0.15) ; frame3->GetYaxis()->SetTitleOffset(1.8) ; frame3->Draw() ;
  frame3->GetYaxis()->SetTitle("Events");
  frame3->SetTitle("");
  //  frame3->SetMaximum(40010);
  frame3->GetXaxis()->SetTitle("#Delta#Phi(E_{T}^{Miss},Jet)");
  //  frame3->GetXaxis()->SetRangeUser(0.5,3.2);

  TLegend* leg2 = new TLegend(0.5, 0.6, 0.9, 0.85);
  leg2->SetBorderSize(0);
  leg2->AddEntry("Data_", "data", "P" );
  leg2->AddEntry("Fit_", "fit", "L" );
  leg2->AddEntry("Zjets_", "Z+jets", "F" );
  leg2->AddEntry("Wjets_", "W+jets", "F" );
  leg2->AddEntry("ttbar_", "ttbar", "F" );
  leg2->AddEntry("VVstop_", "VV+stop", "F" );
  leg2->AddEntry("Multijet_", "multijet", "L" );
  leg2->Draw("same");
  c->SaveAs("Fitting_multijet/FitMultijet_"+region+".png");

  
}

