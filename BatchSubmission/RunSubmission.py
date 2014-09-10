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
    maxpt=["10","200"]
    eta  =["1.75","2.0","2.25","2.50"]
    pdgid=["13","11"]
    
    """ parameters to be replaced in the python file """
    ToReplace=["MAXPT","ETA","PDGID","OUTPUTFILE"]

    
    """ make all combination of the cuts  """
    allCombinations = makestrings(maxpt,eta,pdgid)
    
    """ make postfix for the file names """
    allCombinations_named =  ["_Pt-"+i[0]+"_Eta-"+i[1]+"_ID-"+i[2] for i in allCombinations]
    postfix=[]
    for i in allCombinations_named : postfix.append(''.join(["gen-sim",i]))

    """ output and python file names """
    outputfile=[]
    for i in postfix : outputfile.append(''.join([i,".root"]))
    pythonfile=[]
    for i in postfix : pythonfile.append(''.join(["auto-delete-",i,".py"]))
        

    """ put all the lists into one list which will be used by class to replace the parameters in the python and the batch submission file
    Last element of replaceby is the name of the python file as a result of the changes"""
    ReplaceBy=[]
    for i in range(len(pythonfile)):
        list_ = list(allCombinations[i])
        list_.append(outputfile[i])
        list_.append(pythonfile[i])
        ReplaceBy.append(list_)
    
    
    
    """ Preparing the .py files
    Last element of the list_ should be name of the file produced after the changes """
    for j in range(len(ReplaceBy)):
        obj1 = ReplaceText("SingleMuPt_200_cfi_GEN_SIM.py",ToReplace,ReplaceBy[j])
        obj1.printvalues()
        obj1.MakeChanges(prepareBatchScripts,submitJobs)
    
