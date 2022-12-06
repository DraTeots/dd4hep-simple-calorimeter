import uproot
import matplotlib
import matplotlib.pyplot as plt
import awkward as ak
import hist
import numpy as np
import os
import pandas as pd


def load_as_pandas(root_file_name, entry_start=0, entry_stop=None):
    # Open root file and get "events" tree from it
    tree = uproot.open(root_file_name)["events"]

    # Read fields from a file
    gen_status = tree['MCParticles/MCParticles.generatorStatus'].array(entry_start=entry_start, entry_stop=entry_stop)
    masses = tree['MCParticles/MCParticles.mass'].array(entry_start=entry_start, entry_stop=entry_stop)
    px = tree['MCParticles/MCParticles.momentum.x'].array(entry_start=entry_start, entry_stop=entry_stop)
    py = tree['MCParticles/MCParticles.momentum.y'].array(entry_start=entry_start, entry_stop=entry_stop)
    pz = tree['MCParticles/MCParticles.momentum.z'].array(entry_start=entry_start, entry_stop=entry_stop)
    # pdg = tree['MCParticles/MCParticles.PDG'].array(entry_start=entry_start, entry_stop=entry_stop)
    # pos_x = tree['MCParticles/MCParticles.vertex.x'].array(entry_start=entry_start, entry_stop=entry_stop)
    # pos_y = tree['MCParticles/MCParticles.vertex.y'].array(entry_start=entry_start, entry_stop=entry_stop)
    # pos_z = tree['MCParticles/MCParticles.vertex.z'].array(entry_start=entry_start, entry_stop=entry_stop)

    # 'stable' are particles from particle gun
    stable_only = gen_status > 0

    # filter other particles
    masses = masses[stable_only]
    px = px[stable_only]
    py = py[stable_only]
    pz = pz[stable_only]
    # pdg = ak.flatten(pdg[stable_only]).to_numpy()
    # pos_x = ak.flatten(pos_x[stable_only]).to_numpy()
    # pos_y = ak.flatten(pos_y[stable_only]).to_numpy()
    # pos_z = ak.flatten(pos_z[stable_only]).to_numpy()

    # calculate energy
    energies = np.sqrt(masses * masses + px * px + py * py + pz * pz)
    energies = ak.flatten(energies).to_numpy()
    true_e = energies

    module_edep = tree['WallECalHits/WallECalHits.energy'].array(entry_start=entry_start, entry_stop=entry_stop)
    sum_e = ak.sum(module_edep, axis=1).to_numpy()

    # hits_edep = tree['WallECalHitsContributions/WallECalHitsContributions.energy'].array(entry_start=entry_start,
    #                                                                                      entry_stop=entry_stop)
    #ct_sum_e = ak.sum(hits_edep, axis=1).to_numpy()

    # check all arrays are the same len
    assert len(energies) == len(sum_e)
    #assert len(sum_e) == len(ct_sum_e)
    df = pd.DataFrame({"true_e": true_e,
                       "sum_e": sum_e,
                       #"ct_sum_e": ct_sum_e,
                       "p": ak.flatten(np.sqrt( px * px + py * py + pz * pz)).to_numpy(),
                       "m": ak.flatten(masses).to_numpy()})
    return df


if __name__ == "__main__":
    import argparse

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in-file", "Name of input file")
    parser.add_argument("-o", "--out-file", "Name of output file")
    args = parser.parse_args()
    print(f"Converting file:\n  {args.infile}")
    print(f"Resulting  file:\n  {args.outfile}")

    # Load dataframe
    df = load_as_pandas(args.infile)
    df.to_pickle(args.outfile)





