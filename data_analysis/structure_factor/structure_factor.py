#!/usr/bin/env python
from logger import *
import lattice as lat
import numpy as np
import weight, os, matplotlib
if "DISPLAY" not in os.environ:
    log.info("no DISPLAY detected, switch to Agg backend!")
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

def Reform(Data, NSub, L, Vol):
    Chi = np.ndarray((NSub, NSub, Vol))
    AveChi = np.ndarray((NSub, NSub, Vol))
    for i in range(NSub):
        for j in range(Vol*NSub):
            site = j/4
            sub = j-site*4
            Chi[i][sub][site] = Data[i][j]
    return Chi

def PlotChi_2D(Chi, lat, DoesSave=True):

    #####Pyrochlore
    KList_hhl=[]
    KList_hl0=[]
    for i in range(-lat.L[0]*4, lat.L[0]*4+1):
        for j in range(-lat.L[1]*4, lat.L[1]*4+1):
            for k in range(-lat.L[2]*4, lat.L[2]*4+1):
                kpoint = i*lat.ReciprocalLatVec[0]+j*lat.ReciprocalLatVec[1]+ \
                        k*lat.ReciprocalLatVec[2]
                if np.abs(kpoint[0]-kpoint[1])<1e-5:
                    KList_hhl.append((i,j,k))
                if np.abs(kpoint[2])<1e-5:
                    KList_hl0.append((i,j,k))

    bound=[[-40,40],[-40,40]]
    ######hhl
    k_hhl, ChiK_hhl=lat.FourierTransformation(Chi[:,:,:], \
            KList_hhl, "Integer", bound=bound)
    ChiK_hhl=[e.real for e in ChiK_hhl]

    x_hhl=[]
    y_hhl=[]
    for e in k_hhl:
        x_hhl.append(np.sqrt(2.0)*e[0])
        y_hhl.append(e[2])

    ######hl0
    k_hl0, ChiK_hl0=lat.FourierTransformation(Chi[:,:,:], \
            KList_hl0, "Integer", bound=bound)
    ChiK_hl0=[e.real for e in ChiK_hl0]
    x_hl0=[]
    y_hl0=[]

    for e in k_hl0:
        x_hl0.append(e[0])
        y_hl0.append(e[1])

    plt.figure(1)
    ax1=plt.subplot(121,aspect='equal')
    plt.scatter(x_hhl,y_hhl,c=ChiK_hhl, s=29, edgecolor="black", linewidth=0)
    plt.xlabel("Direction [hh0]")
    plt.ylabel("Direction [00l]")
    plt.xlim(-30, 30)
    plt.ylim(-30, 30)
    label=np.linspace(min(ChiK_hhl),max(ChiK_hhl), 4)

    plt.figure(1)
    ax1=plt.subplot(122,aspect='equal')
    plt.scatter(x_hl0,y_hl0,c=ChiK_hl0, s=29, edgecolor="black", linewidth=0)
    plt.xlabel("Direction [h00]")
    plt.ylabel("Direction [0l0]")
    plt.xlim(-30, 30)
    plt.ylim(-30, 30)
    label=np.linspace(min(ChiK_hl0),max(ChiK_hl0), 4)

    if DoesSave:
        plt.savefig("pyrochlore_chiK_{0}.pdf".format(lat.Name))
    else:
        plt.show()
    plt.close()
    log.info("Plotting done!")

if __name__=="__main__":
    import weight
    import IO
    NSub = 4
    L = 8
    Vol = L*L*L

    WeightPara={"NSublat": NSub, "L":[L,L,L],
            "Beta": 1.0, "MaxTauBin":64}
    Map=weight.IndexMap(**WeightPara)

    l=lat.Lattice("Pyrochlore", Map)

    Data = IO.LoadDict("../static_corr")["Correlations"]
    Chi  = Reform(Data, NSub, L, Vol)
    PlotChi_2D(Chi, l, False)
    PlotChi_2D(Chi, l)

