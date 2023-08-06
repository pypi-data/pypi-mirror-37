"""
utils for plotting correlation matrices
"""

import numpy
import matplotlib.pyplot as plt

def reorder_corrs(corrmtx,labeldata,labels='YeoDesc7'):
    """
    reorder correlation matrix according to network labels
    """

    idx=numpy.lexsort(([i for i in range(labeldata.shape[0])],labeldata[labels]))
    tmp=corrmtx[:,idx]
    return(tmp[idx,:],labeldata.iloc[idx,:])

def plot_reordered_corrs(corrmtx,labeldata,labels='YeoDesc7',
                    colorbar=True,figsize=(10,10)):
    """
    plot correlation matrix after reordering
    """

    corr_reord,labeldata_reord=reorder_corrs(corrmtx,labeldata)
    plt.figure(figsize=figsize)
    plt.imshow(corr_reord)
    # find breakpoints and plot lines
    breaks=numpy.array([int(not i) for i in labeldata_reord[labels].values[:-1]==labeldata_reord[labels].values[1:]])
    breaklocs=numpy.hstack((numpy.where(breaks)[0],numpy.array(corrmtx.shape[0]-1)))
    for b in breaklocs:
        plt.plot([0,corrmtx.shape[0]-1],[b,b],color='w',linewidth=0.5)
        plt.plot([b,b],[0,corrmtx.shape[0]-1],color='w',linewidth=0.5)
    # find label locations
    # add a zero to help find label locations
    breaklocs2=numpy.hstack(([0],breaklocs))
    label_locs=numpy.mean(numpy.vstack((breaklocs,breaklocs2[:-1])),0)
    networks=labeldata_reord[labels].values[breaklocs]
    ax=plt.gca()
    ax.set_yticks(label_locs)
    ax.set_yticklabels(networks)
    if colorbar:
        plt.colorbar()
