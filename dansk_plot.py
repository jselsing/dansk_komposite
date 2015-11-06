#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

from gen_methods import format_axes, medfilt, hist
import numpy as np
import glob

import matplotlib.pylab as pl
import lineid_plot
import seaborn as sns; sns.set_style('ticks')






def main():
    
    #Load composite
    composite = np.array(np.genfromtxt(glob.glob('/Users/jselsing/Work/Projects/QuasarComposite/Selsing2015.dat')[0]))

    wl = composite[:,0]

    flux = composite[:,1] * wl / 10000
    error = composite[:,2]


    from scipy.interpolate import InterpolatedUnivariateSpline as spline
    f = spline(wl[np.where(flux != 0)], flux[np.where(flux != 0)])
    flux = f(wl)
    import scipy.signal as sig
    flux = sig.savgol_filter(flux, 31, 1)




    fig, ax = pl.subplots(figsize=(16,10))
    ax.plot(wl, flux)
    fit_line_positions = np.genfromtxt('linelist.txt', dtype=None)

    linelist = []
    linenames = []
    for n in fit_line_positions:
        linelist.append(n[1])
        linenames.append(n[0])


    import matplotlib as mpl

    ax.set_xlim((700, 7200))
    ax.set_ylim((0, 8))
    format_axes(ax)


    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(16)


    from matplotlib import rcParams
    rcParams['text.usetex']=True
    ax.set_xlabel(r'Hvileb$\textsf{\o}$lgel$\textsf{\oe}$ngde $\textsf{\AA}$')
    ax.set_ylabel(r'Skaleret flux $\lambda$F$_\lambda$')



    pl.tight_layout()




    val = []
    for p in range(len(linelist)):
        xcoord = linelist[p]
        mask = (wl > xcoord - 1) & (wl < xcoord + 1)
        y_val = np.mean((flux)[mask])
        val.append(1.2 * y_val)
    # change_sign = np.ones_like(val)
    # for n in [1, 6, 8, 11, 12, 15]:
    #     change_sign[n] /= 3 
    arrow_tips = val#*change_sign
    lineid_plot.plot_line_ids(wl, (flux), linelist, linenames, arrow_tip=arrow_tips, ax=ax, maxiter=1000)

    for i in ax.lines:
        if '$' in i.get_label():
            i.set_alpha(0.3)
    a = ax.findobj(mpl.text.Annotation)
    for i in a:
        if '$' in i.get_label():
            i.set_size(14)


    pl.savefig('komposit.pdf')
    pl.show()



if __name__ == '__main__':
    main()