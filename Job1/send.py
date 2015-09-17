#!/usr/bin/python
import random
import os, sys
IsCluster=False
sourcedir="../program/"
execute="XXZ"
Dim = 3
Latticename = "Pyrochlore"
homedir=os.getcwd()
filelist=os.listdir(sourcedir)
sourcename=[elem for elem in filelist if elem[-3:]=="f90"]
sourcename.sort()
sourcename=sourcename[-1]
os.system("gfortran "+sourcedir+"/"+sourcename+" -O3 -o "+homedir+"/"+execute)
infilepath=homedir+"/infile"
outfilepath=homedir+"/outfile"
inlist=open(homedir+"/inlist","r")
i=0
nblck=int(inlist.readline().split(":")[1])
nsample=int(inlist.readline().split(":")[1])
nsweep=int(inlist.readline().split(":")[1])
ntoss=int(inlist.readline().split(":")[1])
isload=int(inlist.readline().split(":")[1])
seed=-int(random.random()*1000)
if(os.path.exists(infilepath)!=True):
    os.system("mkdir "+infilepath)
if(os.path.exists(outfilepath)!=True):
    os.system("mkdir "+outfilepath)
for eachline in inlist:
        i+=1
        para=eachline.split()
        for j in range(int(para[-1])):
            seed-=1
            infile="_in"+str(i)+"_"+str(j)
            outfile="_out"+str(i)+"_"+str(j)
            jobfile="_job"+str(i)+"_"+str(j)+".sh"
            f=open(infilepath+"/"+infile,"w")
            item=para[0:-1]
            item.append(str(ntoss))
            item.append(str(nsample))
            item.append(str(nsweep))
            item.append(str(seed))
            item.append(str(nblck))
            item.append(str(isload))
            item.append("_".join(para[2:-1])+"_"+str(j)+".dat")
            stri=" ".join(item)
            f.write(str(Dim)+"\n")
            f.write("Pyrochlore "+stri)
            f.close()

            if IsCluster==False:
                os.system("./"+execute+" < "+infilepath+"/"+infile+" > "+outfilepath+"/"+outfile)
            else:
                with open(jobfile, "w") as fjob:
                    fjob.write("#!/bin/sh\n"+"#PBS -N "+jobname+"\n")
                    if hasattr(job_atom, "pbs_command"):
                        fjob.write(job_atom.pbs_command+"\n")
                    fjob.write("#PBS -o "+homedir+"/Output\n")
                    fjob.write("#PBS -e "+homedir+"/Error\n")
                    fjob.write("echo $PBS_JOBID >>"+homedir+"/id_job.log\n")
                    fjob.write("cd "+homedir+"\n")
                    fjob.write(job_atom.execute+" -f "+infilepath+"/"+infile)

                    os.system("qsub "+jobfile)
                    os.system("rm "+jobfile)
                    print("job "+jobfile+" submitted!")
print("Jobs manage daemon is ended")
sys.exit(0)