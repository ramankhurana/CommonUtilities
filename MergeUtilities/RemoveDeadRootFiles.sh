## in this script change the name of rootfile and treename 
## and run using source RemoveDeadRootFiles.sh
## you should see the number of entries in the tree 
## test this on a dead file and then I can follow up from that point onwards, how to edit the script. 

rootfilename=mlfit.root
treename=tree_fit_sb

root -l <<EOF                                                                                                                                                                        
TFile* f = new TFile("$rootfilename","READ");                                                                                                                                        
f->cd();                                                                                                                                                                             
echo ${treename}->GetEntries()     

EOF                                                                                                                                                                                  
