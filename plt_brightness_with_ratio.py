import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import sys
import pdb


#df=pd.read_csv('temp_sdds_brightness_15_1_1.csv')
df=pd.read_csv('temp_sdds_brightness_143pm.csv')
Brightness_1= [col for col in df if col.startswith('Brightness')]
photonEnergy_1= [col for col in df if col.startswith('photonEnergy')]
 
#dd=pd.read_csv('temp_sdds_brightness_21_1_1_espread_1511.csv')
dd=pd.read_csv('temp_sdds_brightness_144pm.csv')
Brightness_2= [col for col in dd if col.startswith('Brightness')]
photonEnergy_2= [col for col in dd if col.startswith('photonEnergy')]

ax22=df.plot(kind='scatter',y=Brightness_1[0],x=photonEnergy_1[0],color='DarkBlue', marker=".",alpha=.5, logy=1,fontsize=13,label='DTBA_I12')
#ax22=df.plot(kind='scatter',y=Brightness_2[0],x=photonEnergy_2[0],color='red', marker=".",alpha=.5, logy=1,fontsize=13)  
for bbb in range(1,len(Brightness_1)):
    print(bbb)
    type1=df.plot(kind='scatter',y=Brightness_1[bbb],x=photonEnergy_1[bbb],color='DarkBlue',marker=".",ax=ax22, alpha=.5,logy=1,fontsize=13)

for bbb in range(0,len(Brightness_2)):
    print(bbb)
    type2=dd.plot(kind='scatter',y=Brightness_2[bbb],x=photonEnergy_2[bbb],color='red',marker=".",ax=ax22, alpha=.5,logy=1,fontsize=13,label='DTBA_I15')
    ax22.set_xlabel('E (keV)',fontsize=13)
    ax22.set_ylabel('B(phot/s/mm^2/mrad^2/0.1%B.W.)',fontsize=13)
plt.show()
plt.close()

for bbb in range(1,len(Brightness_1)):
    # print(bbb)
    scale_y = df[Brightness_1[bbb]]/dd[Brightness_2[bbb]]
    scale_x = df[photonEnergy_1[bbb]]

    plt.plot(scale_x,scale_y,'b.')
    plt.xlabel('E (keV)')
    plt.ylabel('Ratio')

plt.show()
plt.close()
