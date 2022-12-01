data_base_dir = "/mnt/work/data/epi"
files_set_nov_29_2022 = [
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-1GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-1GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-2GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-2GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-3GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-3GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-4GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-4GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-5GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-5GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-6GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-6GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-7GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-7GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-8GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-8GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-9GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-9GeV-10000events-pi--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-10GeV-10000events-e--40mm-R1450.root",
    "cherepaha_nov-29-2022/SciGlass-4-1-L-13x13-20x20x200mm-10GeV-10000events-pi--40mm-R1450.root",
]


def data_to_pandas():
    import re
    import uproot
    import numpy as np
    import pandas as pd
    
    def read_modules_de(file_name, entry_start = 0, entry_stop = 100000):
        tree = uproot.open(file_name)["tree_crystals"]
        module_de_flat = tree['edep'].array(entry_start=entry_start, entry_stop=entry_stop).to_numpy()
        return module_de_flat

    energy_re = re.compile('.+-(.+)GeV.+')

    # future columns of dataframe
    mom_column = []
    edep_sum_column = []
    prt_name_column = []
    tower_values_column = []

    # iterate over files
    for name in files_set_nov_29_2022:
        print(name)        
        tower_values = read_modules_de(f"{data_base_dir}/{name}")
        edep_sums = np.sum(tower_values, axis=1)
        for i, e_sum in enumerate(edep_sums):
            mom_column.append(float(energy_re.findall(name)[0]))
            prt_name_column.append("e-" if "-e--" in name else "pi-")
            edep_sum_column.append(e_sum)
            tower_values_column.append(tower_values[i])

    df = pd.DataFrame({"p": mom_column, "prt_name": prt_name_column, "de_sum": edep_sum_column, "towers": tower_values_column})
    return df


if __name__ == "__main__":
        
    df = data_to_pandas()
    print(df.head())
    df.to_feather("2022-11-29_cherepaha_SciGlass-4-1-L_13x13_20x20x200mm_1-10GeV_e-pi-_10kev-each.feather")
        

    