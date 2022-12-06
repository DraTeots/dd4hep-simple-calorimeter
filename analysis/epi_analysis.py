import uproot
import matplotlib
import matplotlib.pyplot as plt
import awkward as ak
import hist
import numpy as np
from event_display import gdml_read_ecal_info
import os
import pandas as pd
import matplotlib.patches as mpatches
from scipy.stats import crystalball, norm

from dataclasses import dataclass, asdict, field, InitVar

@dataclass
class Wharrgarbl(object):
    a: int
    b: int
    c: int
    sum: InitVar[int]  # note: InitVar will exclude this from the dict
    version: InitVar[str] = "old"

    def __post_init__(self, sum, version):
        self.sum = 6  # this looks like an OP mistake?
        self.version = str(version)


def make_sigma_separation(e_df, pi_df, title, separ_sigmas=2):
    # Fit with crystalball and gauss
    cb_beta, cb_m, cb_loc, cb_scale = crystalball.fit(e_df.e_div_p, loc=0.6)
    norm_loc, norm_sigma = norm.fit(e_df.e_div_p)
    print(cb_beta, cb_m, cb_loc, cb_scale)
    print(norm_loc, norm_sigma)

    # where we separate
    separ_x = cb_loc - norm_sigma*separ_sigmas
    n_pi_above_num = np.size(pi_df.query(f"e_div_p > {separ_x}").e_div_p)
    n_e_below_num = np.size(e_df.query(f"e_div_p <= {separ_x}").e_div_p)
    n_e_above_num = np.size(e_df.query(f"e_div_p > {separ_x}").e_div_p)

    n_pi_above = n_pi_above_num / np.size(pi_df.e_div_p)
    n_e_below = n_e_below_num / np.size(e_df.e_div_p)
    n_e_above = n_e_above_num / np.size(e_df.e_div_p)

    print(separ_x, n_pi_above, n_e_below, n_e_above, np.size(e_df.e_div_p))

    # We can set the number of bins with the *bins* keyword argument.
    fig, axs = plt.subplots()    
    axs.hist(e_df.e_div_p, bins=50, alpha = 0.5, edgecolor='blue', linewidth=0.3, range=(0, 1), density=True, label="$e^{-}$")
    axs.hist(pi_df.e_div_p, bins=50, alpha = 0.5, edgecolor='red', linewidth=0.3, range=(0, 1), density=True, label="$\pi^{-}$")
    axs.axvline(x=separ_x, color='red', linestyle='--', linewidth=0.8, label=f"peak-{separ_sigmas}$\sigma$ = {separ_x:.2f}")
    axs.plot([], [], ' ', label="$\epsilon_{e^{-}}$ = " + f"{n_e_above*100:.2f}%")
    axs.plot([], [], ' ', label="$\epsilon_{\pi^{-}}$ = " + f"{n_pi_above*100:.2f}%")
    axs.legend(loc='best')
    axs.set_title(f"{title} <E> = {e_df.p.mean():.1f} GeV")
    # txt = ax.text(0.5, 0.5, f"{separ_x}\n {n_pi_above}, {n_e_below}, {n_e_above}")
    # txt.set_clip_on(False)
    # handles, labels = plt.get_legend_handles_labels()
    # handles.append(mpatches.Patch(color='none', label=extraString))
    # plt.legend(handles=handles)
    # # txt.set_clip_on(False)  # this will turn clipping off (always visible)
    # plt.plot()
    return cb_loc, norm_sigma, separ_x, n_e_above_num, n_e_above, n_pi_above_num, n_pi_above, n_e_below_num, n_e_below, axs


def df_make_separation(df, e_center, title, separ_sigmas=2,  range=1):
    e_min = e_center - 0.5*range
    e_max = e_center + 0.5*range
    e_filtered_df = df.query(f"({e_min} < p < {e_max}) and prt_name=='e-'")
    pi_filtered_df = df.query(f"({e_min} < p < {e_max}) and prt_name=='pi-'")

    make_sigma_separation(e_filtered_df, pi_filtered_df, title=title, separ_sigmas=separ_sigmas)
