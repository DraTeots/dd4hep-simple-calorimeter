from dd4hep_root_reader import load_as_pandas
import re
import uproot
import numpy as np
import pandas as pd



if __name__ == "__main__":
    base_dir = "/home/romanov/work/data/epi"
    input_files = [
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_e-_wall_only_e0.7-0.7GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_pi-_wall_only_e0.7-0.7GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_e-_wall_only_e1-1GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_pi-_wall_only_e1-1GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_e-_wall_only_e2-2GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_pi-_wall_only_e2-2GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_e-_wall_only_e3-3GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_pi-_wall_only_e3-3GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_e-_wall_only_e5-5GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_pi-_wall_only_e5-5GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_e-_wall_only_e10-10GeV_center_1prt_20000evt.edm4hep.root",
        f"{base_dir}/2022-12-02_pgun_SciGlass-2x2x40_pi-_wall_only_e10-10GeV_center_1prt_20000evt.edm4hep.root",
    ]

    # future columns of dataframe
    mom_column = []
    edep_sum_column = []
    prt_name_column = []
    tower_values_column = []

    for name in input_files:        
        print(f"{name}\n")
        df = load_as_pandas(name)
        
        # tower_values = read_modules_de(f"{data_base_dir}/{name}")        
        for i, e_sum in enumerate(df.sum_e):
            if not i%1000:
                print(i)
            mom_column.append(df.p[i])
            prt_name_column.append("e-" if "_e-_" in name else "pi-")
            edep_sum_column.append(e_sum)
            tower_values_column.append([0,0])

        df = pd.DataFrame({"p": mom_column, "prt_name": prt_name_column, "de_sum": edep_sum_column, "towers": tower_values_column})
    
    output_file ="2022-11-29_dd4hep_PbWO4_13x13_20x20x200mm_0-10GeV_e-pi-_100kev.feather"
    df.to_feather(output_file)