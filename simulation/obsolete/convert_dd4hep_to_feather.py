from dd4hep_root_reader import load_as_pandas

if __name__ == "__main__":
    base_dir = "/home/romanov/work/data/epi"
    input_files = [
        f"{base_dir}/2022-11-22_pgun_e-_wall_only_e0.01-10GeV_center_1prt_10000evt.edm4hep.root",
        f"{base_dir}/2022-11-22_pgun_pi-_wall_only_e0.01-10GeV_center_1prt_10000evt.edm4hep.root",
        f"{base_dir}/2022-11-23_pgun_PbWO4_e-_wall_only_e0.01-10GeV_center_1prt_10000evt.edm4hep.root",
        f"{base_dir}/2022-11-23_pgun_PbWO4_pi-_wall_only_e0.01-10GeV_center_1prt_10000evt.edm4hep.root",
    ]

    for input_file in input_files:
        output_file = input_file.replace(".edm4hep.root", ".feather")
        print(f"Converting file:\n  in  : {input_file}\n  out : {output_file}")
        df = load_as_pandas(input_file)
        df.to_feather(output_file)