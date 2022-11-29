import uproot
import matplotlib
import matplotlib.pyplot as plt
import awkward as ak
import hist
import numpy as np
from event_display import gdml_read_ecal_info
import os
import pandas as pd

#matplotlib.rc("figure", dpi=200)

dir_path = os.path.dirname(os.path.realpath("__file__"))
print(f"Believed path is: {dir_path}")

from event_display import table_display

"""
mmap_mode{None, ‘r+’, ‘r’, ‘w+’, ‘c’}, optional
A memory-mapped array is kept on disk. However, it can be accessed and sliced like any ndarray. 
Memory mapping is especially useful for accessing small fragments of large files without reading the entire file into memory.
"""
npz_file = np.load(f'{dir_path}/2022-11-22_pgun_e-_wall_only_e0.01-10GeV_center_1prt_10000evt.npz', mmap_mode="r+")

print([key for key in npz_file.keys()])

modules = npz_file['modules'][0:100]

# Load geometry file
ecal_info = gdml_read_ecal_info(f"{dir_path}/wall_only.gdml")

# ecal_info is of EcalGeoInfo class, which is a helper holding information
# about all needed ecal geometries.
# Print what information it holds:
ecal_info.print()


# We can plot this mask with matplotlib, which the most self-describing:
pics_prefix = "event_plots/13x13/event_"

for i, event in enumerate(modules):
    print(f"creating {i}")
    fig, ax = plt.subplots(figsize=(8, 8))
    ecal_info.mpl_plot_event(np.reshape(event, (13, 13)), ax)
    fig.savefig(f"{pics_prefix}{i}", transparent=False)
    del fig

#events = npz_file[:100]



# data = [npz_file[key] for key in npz_file]
# print(npz_file)
# print(data)

# printout shape
#print(f"Inputs shape new = {np.shape(input_data)}")
#
# for i in range(100):
#     true_event = np.exp(input_data[i]*11)
#     fig, ax = table_display(true_event)
#     fig.savefig(f"{pics_prefix}{i}", transparent=False)
#     del fig