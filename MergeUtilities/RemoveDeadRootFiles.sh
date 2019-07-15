## in this script change the name of rootfile and treename 
## and run using source RemoveDeadRootFiles.sh
## you should see the number of entries in the tree 
## test this on a dead file and then I can follow up from that point onwards, how to edit the script. 

dirname="/eos/cms/store/user/khurana//ExoPieInputs/MergedSkims/Merged_tDM_06052019/"

ls -1 $dirname > files.txt
filelist=`cat files.txt`
treename='outTree'


for which in  $filelist  ; do

    rootfilename=$dirname/$which
    echo $which
    root -l <<EOF                                                                                                                                                                                           
                                                                                                                                                                                                            
    TFile* f = new TFile("$rootfilename","READ");                                                                                                                                                           
    f->cd();                                                                                                                                                                                                
                                                                                                                                                                                                            
     ${treename}->GetEntries()                                                                                                                                                                              
EOF

done


