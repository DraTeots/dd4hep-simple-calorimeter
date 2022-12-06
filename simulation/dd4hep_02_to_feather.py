from dd4hep_root_reader import load_as_pandas
import re
import uproot
import numpy as np
import pandas as pd
import hist

data_set_2022_12_05_pbwo4 = [
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_e-_wall_only_e0.7-0.7GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_pi-_wall_only_e0.7-0.7GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_e-_wall_only_e1-1GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_pi-_wall_only_e1-1GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_e-_wall_only_e2-2GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_pi-_wall_only_e2-2GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_e-_wall_only_e3-3GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_pi-_wall_only_e3-3GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_e-_wall_only_e4-4GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_PbWO4_2x2x20_pi-_wall_only_e4-4GeV_center_1prt_20000evt.edm4hep.root",
]

data_set_2022_12_05_sciglass = [
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_SciGlass_2x2x40_e-_wall_only_e0.7-0.7GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_SciGlass_2x2x40_pi-_wall_only_e0.7-0.7GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_SciGlass_2x2x40_e-_wall_only_e1-1GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_SciGlass_2x2x40_pi-_wall_only_e1-1GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_SciGlass_2x2x40_e-_wall_only_e2-2GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_SciGlass_2x2x40_pi-_wall_only_e2-2GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_SciGlass_2x2x40_e-_wall_only_e3-3GeV_center_1prt_20000evt.edm4hep.root",
    "/home/romanov/work/data/epi/21x21/2022-12-05_pgun_SciGlass_2x2x40_pi-_wall_only_e3-3GeV_center_1prt_20000evt.edm4hep.root",
]

def edm4hep_to_feather(input_files, output_file):
    
    # future columns of dataframe
    mom_column = []
    edep_sum_column = []
    prt_name_column = []
    tower_values_column = []

    for name in input_files:        
        print(f"{name}\n")
        df = load_as_pandas(name)
        
        # tower_values = read_modules_de(f"{data_base_dir}/{name}")        
        for i, (e_sum, p) in enumerate(zip(df.sum_e, df.p)):
            # print(e_sum)
            # if i==10:
            #     print(i)
            #     exit()
            
            # print(p)
            mom_column.append(p)
            prt_name_column.append("e-" if "_e-_" in name else "pi-")
            edep_sum_column.append(e_sum)
            tower_values_column.append([0,0])

        df = pd.DataFrame({"p": mom_column, "prt_name": prt_name_column, "de_sum": edep_sum_column, "towers": tower_values_column})
    df.to_feather(output_file)
    print(f"Saved to:\n{output_file}")    
    return df


if __name__ == "__main__":
    base_dir = "/home/romanov/work/data/epi/21x21"

    edm4hep_to_feather(data_set_2022_12_05_pbwo4, f"{base_dir}/2022-12-05_pgun_PbWO4_2x2x20_e-_wall_only_e0.7-3GeV_center_1prt_20000evt.feather")
    edm4hep_to_feather(data_set_2022_12_05_sciglass, f"{base_dir}/2022-12-05_pgun_SciGlass_2x2x40_e-_wall_only_e0.7-3GeV_center_1prt_20000evt.feather")
