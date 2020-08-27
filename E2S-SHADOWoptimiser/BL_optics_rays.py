#
# Python script to run shadow3. Created automatically with ShadowTools.make_python_script_from_list().
#

import sys
import glob
import time
import os
import ShadowTools
import numpy
import re
import subprocess

os.environ['LD_LIBRARY_PATH'] = '/E2S_JL/E2S-SHADOWoptimiser/shadow3/'
sys.path.append('/E2S_JL/E2S-SHADOWoptimiser/shadow3/build/lib.linux-x86_64-3.7/')#JL: export the lib and python path to run it in cluster

import Shadow


#sys.path.insert(0, '/dls/physics/students/sug89938/shadow_srw/')


# write (1) or not (0) SHADOW files start.xx end.xx star.xx

def GetLastFile(path):
    print('Now in the GetLastFile function...')
    list_of_files = glob.glob(path) 
    mostRecentFile = max(list_of_files, key=os.path.getctime)
    print('we are going to read the solution...')
    return mostRecentFile


def search(path,keyword):
    content= os.listdir(path)
    for each in content:
        each_path = path+os.sep+each
        if keyword in each:
           print(each_path)
        if os.path.isdir(each_path):
           search(each_path,keyword)
    return each_path

def BLoptics(par1,par2,par3,par4,par5,par6,par7):
    #time.sleep(2)
    infile = open('shadow.input', 'r')
    
    variables =[]; values=[];
    for line in infile:
        # Typical line: variable = value
        variable, value = line.split('=')
        variable = variable.strip()  # remove leading/traling blanks
        value    = value.strip()
        variables.append(variable)
        values.append(value)
    
    infile.close()
    
    dict={}              # create a dictionary for easy access to variables 
     
    for i in range(0,len(variables)) :
        dict[variables[i]] = values[i]
    
    
    print('this is the function to read current beamline parameters')
    #***********parameters*******************
    a  = float(dict[par1])
    b  = float(dict[par2])
    c  = float(dict[par3])
    d  = float(dict[par4])
    e  = float(dict[par5])
    f  = float(dict[par6])
    g  = float(dict[par7])
    print('par1,par2,par3,par4,par5,par6,par7',a,b,c,d,e,f,g)

    return [a,b,c,d,e,f,g]
#JL : backup method ,do not use-----------------------------------------------

def update_BL(par1,par2,par3,par4,par5,par6,par7,k1,k2,k3,k4,k5,k6,k7):
	time.sleep(2)
	inF  = "/E2S_JL/E2S-SHADOWoptimiser/shadow.input"
	outF = "/E2S_JL/E2S-SHADOWoptimiser/shadow_new.input"
#>>> list
#[1, 2, 3, 4, 5]
#>>> dict = {par1:k1, par2=k1,par3=k1}
#rep = [dict[par1] if par1 in dict else par1 for par1 in line]

	fout = open(outF,"w")
	for line in open(inF,'r').readlines():
		line = re.sub(r'oe5.T_SOURCE .+', r'oe5.T_SOURCE     = '+str(k1), line)
		line = re.sub(r'oe4.T_SOURCE .+', r'oe4.T_SOURCE     = '+str(k2), line)
		line = re.sub(r'oe4.T_SOURCE .+', r'oe4.T_SOURCE     = '+str(k3), line)
		line = re.sub(r'oe5.R_MIN .+', r'oe5.R_MIN     = '+str(k4), line)
		line = re.sub(r'oe5.T_SOURCE .+', r'oe5.T_SOURCE     = '+str(k5), line)
		line = re.sub(r'oe4.T_SOURCE .+', r'oe4.T_SOURCE     = '+str(k6), line)
		line = re.sub(r'oe5.R_MIN .+', r'oe5.R_MIN     = '+str(k7), line)
		fout.writelines(line)
	fout.close()


	print('New Beamline created')
	print('Verification :values after modification:')
	print(k1)
	print(k2)
	print(k3)
#-----------------------------------------------------------------------------------------------------------    

def Calcrays(k1,k2,k3,k4,k5,k6,k7,rootnumber):
#print(par)
#Run SHADOW to create the source and optics
	rootnumber=rootnumber
	#time.sleep(2)
	inF  = "/E2S_JL/E2S-SHADOWoptimiser/shadow.input"
	outF = "/E2S_JL/E2S-SHADOWoptimiser/shadow_run"+rootnumber+".py"
	fout = open(outF,"w")
	fout.write('\nimport Shadow\n')
	fout.write('\nimport numpy\n')
	fout.write('\nimport ShadowTools\n')
	for line in open(inF,'r').readlines():
		line = re.sub(r'oe9.T_SOURCE .+', r'oe9.T_SOURCE     = '+str(k1), line)#update_BL_old JL need to be change for different parameters
		line = re.sub(r'oe10.T_SOURCE .+', r'oe10.T_SOURCE     = '+str(k2), line)
		line = re.sub(r'oe10.T_IMAGE .+', r'oe10.T_IMAGE     = '+str(k3), line)
		line = re.sub(r'oe9.SSOUR .+', r'oe9.SSOUR     = '+str(k4), line)
		line = re.sub(r'oe9.SIMAG .+', r'oe9.SIMAG     = '+str(k5), line)
		line = re.sub(r'oe10.SSOUR .+', r'oe10.SSOUR     = '+str(k6), line)
		line = re.sub(r'oe10.SIMAG .+', r'oe10.SIMAG     = '+str(k7), line)
		fout.write(line)
	fout.write('\nbeam.genSource(oe0)\n')
	fout.write('\nbeam.traceOE(oe1,1)\n')
	fout.write('\nbeam.traceOE(oe2,2)\n')
	fout.write('\nbeam.traceOE(oe3,3)\n')
	fout.write('\nbeam.traceOE(oe4,4)\n')
	fout.write('\nbeam.traceOE(oe5,5)\n')
	fout.write('\nbeam.traceOE(oe6,6)\n')
	fout.write('\nbeam.traceOE(oe7,7)\n')
	fout.write('\nbeam.traceOE(oe8,8)\n')
	fout.write('\nbeam.traceOE(oe9,9)\n')
	fout.write('\nbeam.traceOE(oe10,10)\n')
	#fout.writelines('\nShadowTools.plotxy(beam,1,3,nbins=101,nolost=1,title="Real space")')
	fout.writelines(['\nShadowTools.plotxy(',str(rootnumber),',beam,1,3,nbins=101,nolost=1,title="Real space")'])
	fout.close()

	
	arg='python shadow_run'+str(rootnumber)+'.py'#JL for every chrom have one main run
	subprocess.call(arg, shell=True)


	objectfile=GetLastFile('/E2S_JL/E2S-SHADOWoptimiser/objects/nsgaTest_'+str(rootnumber)+'*')
	#objectfile=search('/dls/physics/students/sug89938/shadow_srw/objects/','nsgaTest_'+str(rootnumber))
	f= open(objectfile,'r')
	data = f.readlines()
	intensity=float(data[0])
	fwhmh=float(data[1])
	fwhmv=float(data[2])
	f.close

	return fwhmh,fwhmv



 


        
	#INPUT_file = sys.argv[1]
	#infile = open(INPUT_file, 'r')
 





	#for lines in lines:
   #		if "oe0" in lines:
   #                      line0 = re.sub(r'oe0.', r'', lines)
   #                      print(line0)              
   #                      Shadow.Source(line0)
   #		if "oe1" in lines:
   #                     #print(lines)
   #                     #oe1 = Shadow.OE()
   #                      line1 = re.sub(r'oe1.', r'', lines)
   #                      oe1=Shadow.Source(line1)
  # 		if "oe2" in lines:
  #                      #print(lines)
  #                      #oe2=str(lines)
  #                       line2 = re.sub(r'oe2.', r'', lines)
  #                       oe2=Shadow.Source(line2)
  # 		if "oe3" in lines:
  #                      #print(lines)
  #                      #oe3=str(lines)
  #                       line3 = re.sub(r'oe3.', r'', lines)
  #                       oe3=Shadow.Source(line3)
     
	#infile.readlines()

	






#choose the target parameters
	#oe=[]
	#oe.append(oe1.RDSOUR)
	#oe.append(oe1.Z_SOUR_ROT)
	#oe.append(oe2.PARAM)
	#print('target parameters',oe)






# Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
# Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")



#BLoptics('oe1.RDSOUR','oe1.Z_SOUR_ROT','oe2.PARAM')

    
