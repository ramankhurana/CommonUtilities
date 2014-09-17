from MakeChanges import *
import itertools
""" This is the main code which will be always task specific. 
There are lists to be filled with values to be seen in the file. 
There is module which will combine these lists into one list. 
Send this list to the replace function and prepare the file. 
This can be done for various files in the main code. 
########################################################################################################################################################
######################################### NOTE : Last element of the list_ should be name of the file produced after the changes ###################
########################################################################################################################################################
"""
def makestrings(*arg):
    allcomb=[]
    size = len(arg)
    for element in itertools.product(*arg):
        allcomb.append(element)
    return allcomb

        

if __name__ == "__main__":
    
    """ --------------   User defined changes -------------- """
    prepareBatchScripts = True 
    submitJobs          = True
    
    """ these lists will be replaced in the text files """
    TauValue=["0.0","5.0","10.0","15.0","20.0"]
    
    """ parameters to be replaced in the python file """
    ToReplace=["TAUVALUE","INPUTFILE", "OUTPUTFILE"]
    
    InputFileName=["gen-sim_Pt-10_Eta-1.75_ID-11.root",
                   "gen-sim_Pt-10_Eta-1.75_ID-13.root",
                   "gen-sim_Pt-10_Eta-2.0_ID-11.root",
                   "gen-sim_Pt-10_Eta-2.0_ID-13.root",
                   "gen-sim_Pt-10_Eta-2.25_ID-11.root",
                   "gen-sim_Pt-10_Eta-2.25_ID-13.root",
                   "gen-sim_Pt-10_Eta-2.50_ID-11.root",
                   "gen-sim_Pt-10_Eta-2.50_ID-13.root",
                   "gen-sim_Pt-200_Eta-1.75_ID-11.root",
                   "gen-sim_Pt-200_Eta-1.75_ID-13.root",
                   "gen-sim_Pt-200_Eta-2.0_ID-11.root",
                   "gen-sim_Pt-200_Eta-2.0_ID-13.root",
                   "gen-sim_Pt-200_Eta-2.25_ID-11.root",
                   "gen-sim_Pt-200_Eta-2.25_ID-13.root",
                   "gen-sim_Pt-200_Eta-2.50_ID-11.root",
                   "gen-sim_Pt-200_Eta-2.50_ID-13.root"]
    
    
    """ Change the input file name such that it can be used to construct output file name """
    inputfilenames_changed = [w.replace(".root","") for w in InputFileName]
    inputfilenames_changed = [w.replace("gen-sim","gen-sim-digi") for w in inputfilenames_changed]
    
    """ make all combination of the cuts  """
    allCombinations = makestrings(TauValue, InputFileName)
    
    """ this is the list being used to construct names """
    allCombinations_names = makestrings(TauValue, inputfilenames_changed)
    
    """ make list for the file names using allCombinations_names """
    allCombinations_named =  [i[1]+"_TauValue-"+i[0] for i in allCombinations_names]
    
    """ make postfix for the file names using allCombinations_names """
    postfix=[]
    #for i in allCombinations_named : postfix.append(''.join(["gen-sim-digi-SingleEle-Pt-10.0_Eta-2.0_140PU_",i]))
    for i in range(len(allCombinations_named)) : postfix.append(''.join([allCombinations_named[i],"_"]))
    
    """ output and python file names """
    outputfile=[]
    for i in postfix : outputfile.append(''.join([i,".root"]))
    pythonfile=[]
    #for i in postfix : pythonfile.append(''.join(["auto-delete-140PU-",i,".py"]))
    for i in postfix : pythonfile.append(''.join(["auto-delete-",i,".py"]))
        

    """ put all the lists into one list which will be used by class to replace the parameters in the python and the batch submission file
    Last element of replaceby is the name of the python file as a result of the changes"""
    ReplaceBy=[]
    for i in range(len(pythonfile)):
        list_ = list(allCombinations[i])
        list_.append(outputfile[i])
        list_.append(pythonfile[i]) ## this should be always last element of list
        ReplaceBy.append(list_)
    
    
    
    """ Preparing the .py files
    Last element of the list_ should be name of the file produced after the changes """
    for j in range(len(ReplaceBy)):
        #obj1 = ReplaceText("step2_DIGI_L1_DIGI2RAW_PU.py",ToReplace,ReplaceBy[j])
        obj1 = ReplaceText("step2_DIGI_L1_DIGI2RAW.py",ToReplace,ReplaceBy[j])
        obj1.printvalues()
        obj1.MakeChanges(prepareBatchScripts,submitJobs)
    
