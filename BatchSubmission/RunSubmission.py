class ReplaceText:
    """class to replace the text in a template file which will be used to produce events"""

    def __init__(self, filename, toreplace, replaceby):
        self.filename     = filename
        self.toreplace    = toreplace
        self.replaceby    = replaceby
        
    def MakeChanges(self):
        fout = open("output.py","a")
        fin = open(self.filename,'r')
        for iline in fin:
            for itoreplace in range(len(self.toreplace)):
                iline = iline.replace(self.toreplace[itoreplace], self.replaceby[itoreplace] )
            fout.write(iline) ## write the changed line after replacement
        fout.close()
        fin.close()
    

    def printvalues(self):
        print self.filename
        print self.toreplace
        print self.replaceby
        

if __name__ == "__main__":
    
    maxpt=["0.51","1.01"]
    minpt=["0.50","1.00"]
    postfix=["500MeV","1000MeV"]
    outputfile=[]
    for i in postfix: outputfile.append(''.join(["gen-sim-events",i,".root"]))
    
    ReplaceBy=[]
    for i in range(len(maxpt)):
        list_ = [maxpt[i],minpt[i],outputfile[i]]
        ReplaceBy.append(list_)
        
    ToReplace=["MAXPT","MINPT","OUTPUTFILE"]
    
    for j in range(len(ReplaceBy)):
        obj1 = ReplaceText("TemplateCfg.py",ToReplace,ReplaceBy[j])
        obj1.printvalues()
        obj1.MakeChanges()
