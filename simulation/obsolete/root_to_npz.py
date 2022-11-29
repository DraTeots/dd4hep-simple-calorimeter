import time

import uproot
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from matplotlib import cm
from matplotlib.colors import LogNorm, Normalize
import awkward as ak
import numpy as np

matplotlib.rc("figure", dpi=200)

from event_display import gdml_read_ecal_info, build_calorimeter_section, mpl_plot_mask, mpl_plot_hits, mpl_plot_event_array

import os
dir_path = os.path.dirname(os.path.realpath("__file__"))
print(dir_path)

# Load geometry file
ecal_info = gdml_read_ecal_info(f"{dir_path}/wall_only.gdml")

# ecal_info is of EcalGeoInfo class, which is a helper holding information
# about all needed ecal geometries.
# Print what information it holds:
ecal_info.print()

# Data file name
#data_file_name = f"{dir_path}/data/test_gun.edm4hep.root"
data_file_name = f"{dir_path}/2022-11-22_pgun_e-_wall_only_e0.01-10GeV_center_1prt_1000evt.edm4hep.root"
output_file = data_file_name.replace(".edm4hep.root", ".npz")

parse_start = time.time()
events = ecal_info.read_events_from_file(data_file_name, 0, 1000)
parse_end = time.time()
print(f"Total events prepare time = {parse_end - parse_start:.3f} [sec]")
print(f"Events processed: {len(events)}")

original_shape = np.shape(events)
print(f"Original shape {original_shape}")

flatten_shape = (original_shape[0], original_shape[1] * original_shape[2])
print(f"Flatten shape {flatten_shape}")
reshaped_events = np.reshape(events, flatten_shape)


np.savez_compressed(output_file, modules=reshaped_events, true_e=energies, true_x=pos_x, true_y=pos_y, true_pdg=pdg)
original_shape = np.shape(events)
print(f"Original shape {original_shape}")

flatten_shape = (original_shape[0], original_shape[1] * original_shape[2])
print(f"Flatten shape {flatten_shape}")
reshaped_events = np.reshape(events, flatten_shape)