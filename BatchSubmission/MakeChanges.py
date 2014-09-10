import os
class ReplaceText:
    """class to replace the text in a template file which will be used to produce events"""

    def __init__(self, filename, toreplace, replaceby):
        self.filename     = filename
        self.toreplace    = toreplace
        self.replaceby    = replaceby
        
        
    def MakeChanges(self, PrepareBatchFiles, SubmitJobs):
        size = len(self.replaceby)
        fout = open(self.replaceby[size-1],"a")
        fin = open(self.filename,'r')
        for iline in fin:
            for itoreplace in range(len(self.toreplace)):
                iline = iline.replace(self.toreplace[itoreplace], self.replaceby[itoreplace] )
            fout.write(iline) ## write the changed line after replacement
        fout.close()
        fin.close()
        
        shellfilename=[]
        if(PrepareBatchFiles): 
            pythonfilename=self.replaceby[size-1]
            shellfilename=pythonfilename.replace(".py",".sh")
            fbout = open(shellfilename,"a")
            fbout.write("#!/bin/sh \n")
            fbout.write("export SCRAM_ARCH=slc6_amd64_gcc472 \n")
            currentpath=os.getcwd()
            fbout.write("cd "+str(currentpath)+" \n")
            fbout.write("eval `scram runtime -sh` \n")
            fbout.write("cmsRun "+pythonfilename+" \n")
            nitemstoreplace = len(self.replaceby)
            fbout.write("xrdcp /tmp/khurana/"+self.replaceby[nitemstoreplace-2]+" root://eoscms.cern.ch///store/user/khurana/HGCAL/GenSim/SingleParticle/"+self.replaceby[nitemstoreplace-2]+" \n")
            fbout.close
            
        if(SubmitJobs):
            print shellfilename
            os.system('chmod 777 '+shellfilename)
            cmnd = 'bsub  -q 1nw '+' '+shellfilename+';'
            os.system(cmnd)

            
    def printvalues(self):
        print self.filename
        print self.toreplace
        print self.replaceby
        
