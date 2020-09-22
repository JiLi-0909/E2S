import glob
import numpy as np
import matplotlib.pyplot
import sys

def read_data_file(filin):
    f = open(filin,'r')
    header = {}
#for i in range(0, 100):
    flag = 1
    i    = 0
    while flag > 0:
        linea     = f.readline()
        if linea[0] is '#':
            header[i] = linea
            if 'Flux' in header[i]:
                text = header[i].strip('#')
                ts   = text.split()
                text = ts[0]+' '+ts[1]

            if 'Intensity' in header[i]:
                text = header[i].strip('#')
                ts   = text.split()
                text = ts[0]+' '+ts[1]


            if 'Initial Photon Energy' in header[i]:
                lin     = header[i].strip()
                col     = lin.split()
                Emin = col[0]
                Emin = Emin[1:]
                emin = float(Emin)
   

            if 'Final Photon Energy' in header[i]:
                lin     = header[i].strip()
                col     = lin.split()
                Emax = col[0]
                Emax = Emax[1:]
                emax = float(Emax)

            if 'Number of points vs Photon Energy' in header[i]:
                lin     = header[i].strip()
                col     = lin.split()
                Epoints = col[0]
                Epoints = Epoints[1:]
                epoints = int(Epoints)
                        
            i = i + 1
                        
        else:
            flag = -1 
  


# Loop over lines and extract variables of interest
    cnt = 0
    data = []
    columns = linea.split()
    data.append(float(columns[0]))  # the first data.append is on the linea 
    
    for line in f:
        line = line.strip()
        columns = line.split()
        
    
        data.append(float(columns[0]))
        cnt=cnt+1
        
    f.close()
    
    Z = data
        
    I=np.array(Z)

    return I#,header,text,emin


#########create the first output file##############
a=0
b=10000

files = sorted(glob.glob('/E2S_JL/e2s_SRW/SRW_I20/multi*.dat'))       ###JL:searching directory###
Fir = files[a:a+1]
for Fir in Fir:
	I,header,ylabel,E = read_data_file(Fir)
	Inew=I
	f = open('SUM_source_20.dat', 'w')  ##JL:define the name of output file with sum intensities##
	for i in xrange(len(header)):
 		f.write(str(header[i]))
	for i in xrange(len(I)):
    		f.write((str(Inew[i]))+'\n')
	f.close()


######## sum data (for power calculation) ######
files = sorted(glob.glob('/E2S_JL/e2s_SRW/SRW_I20/multi*.dat'))       ####JL:searching directory###
filenames = files[a+1:b]
for f in filenames:
    I1,header1,ylabel1,E1 = read_data_file(f)
    SUM = 'SUM_source_20.dat'
    I2,header2,ylabel2,E2 = read_data_file(SUM)
    print(E1)
    I1new=I1
    I2new=I2   
    M = (np.array(I1new),np.array(I2new))   
    Itot = np.sum(M,axis=0)
    f = open('SUM_source_20.dat', 'w')
    for i in xrange(len(header2)):
        f.write(str(header2[i]))
    for i in xrange(len(Itot)):
    	f.write((str(Itot[i]))+'\n')
    f.close()



###########################  average data(if needed)  ###################################################

 


#    for i in xrange(len(I1)):
#        I1_new=I1[i]*E1
#    for i in xrange(len(I2)):
#        I2_new=I2[i]*E2       #




