#include "TH2D.h"
#include "TH1D.h"
#include "TF1.h"
#include <vector>
#include <iostream>
#include "TMath.h"
#include "TGraphAsymmErrors.h"
using namespace std;

Double_t powerlaw(Double_t *x,Double_t* par)
{
  return par[0]*TMath::Power(x[0]/par[1],-1*par[2]); 
}

TH2D* getConvolvedHist(TH2D* h_Migration_Original,TGraphAsymmErrors* EA_ori,Double_t Fnorm, Double_t index, Double_t E0=0.15)
{


 
  
 Double_t log_E0 =TMath::Log(E0); 
 
 TH2D* h_Migration_P = (TH2D*)h_Migration_Original->Clone("P");   
 h_Migration_P->Reset();
 TH2D* h_Flux_A      = (TH2D*)h_Migration_Original->Clone("FA");;   
 h_Flux_A->Reset(); 

 Int_t nBinsX = h_Migration_Original->GetNbinsX();
 Int_t nBinsY = h_Migration_Original->GetNbinsY();
 // Generate Migration PDF 
 for(int xb = 1;xb<=nBinsX;xb ++)
 {
  Double_t norm= 0; 
  for(int yb=1;yb<=nBinsY;yb++)
  {
    norm += h_Migration_Original->GetBinContent(xb,yb);
  }
  if(norm ==0) continue;
  else{
      for(int yb=1;yb<=nBinsY;yb++)
      {

       Double_t p = h_Migration_Original->GetBinContent(xb,yb)/norm;
       h_Migration_P->SetBinContent(xb,yb,p);    
      }
  } 
   
 }
 // Generate FA
 TGraphAsymmErrors* EA = (TGraphAsymmErrors*)EA_ori->Clone("EA_Clone") ; 
 TAxis* xAxis = h_Migration_Original->GetXaxis();
 TAxis* yAxis = h_Migration_Original->GetYaxis();
 Double_t logElow  = xAxis->GetBinCenter(1);
 Double_t logEhigh = xAxis->GetBinCenter(nBinsX); 
 Double_t deltaLogE =yAxis->GetBinCenter(2) - yAxis->GetBinCenter(1); 
 TF1* PL = new TF1("PL",powerlaw,TMath::Power(10,logElow),TMath::Power(10,logEhigh),3);

 PL->SetParameter(0,Fnorm);
 PL->SetParameter(1,E0);
 PL->SetParameter(2,index);
 PL->Eval(1.0);
 Double_t ln10 = TMath::Log(10);
 for(int xb = 1;xb<=nBinsX;xb ++)
 {

  for(int yb=1;yb<=nBinsY;yb++)
  {
   Int_t Bin= h_Migration_Original->GetBin(xb,yb); 
   Double_t E,Eprime,val,Eprimelog;
   E = TMath::Power(10,xAxis->GetBinCenter(xb));
   Eprimelog = yAxis->GetBinCenter(yb);
   Eprime = TMath::Power(10,Eprimelog);
   if(E > 0.1 && E < 100)
   val = E*
         EA->Eval(Eprimelog)*
         PL->Eval(E)*
         h_Migration_P->GetBinContent(xb,yb)*ln10/deltaLogE;
   else
    val =0;
   if(val < 0) val =0;
   h_Flux_A->SetBinContent(xb,yb,val);   
  }
 }
 
 delete EA; 
 delete h_Migration_P;
 return h_Flux_A;
}

