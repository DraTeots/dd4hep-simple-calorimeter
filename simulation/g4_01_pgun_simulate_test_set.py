from g4_pgun_simulation import *

if __name__ == "__main__":

    should_upload = False

    for energy_gev in [0.5, 0.7, 1, 2, 3, 5, 10]:
        for glass_type in ["SciGlass-4-1-L"]:

            # 1 electron
            cfg = G4SimConfig()
            cfg.executable = '/home/romanov/eic/kak-bog-cherepahu/glass-prototype/cmake-build-debug/cherepaha'
            cfg.energy = energy_gev
            cfg.output_dir = "/mnt/work/data/epi"
            cfg.particle = "e-"
            cfg.crystal_type = glass_type
            cfg.events_num = 20000
            run_simulation(cfg, should_upload)

            # 1 pion
            cfg.particle = "pi-"
            cfg.events_num = 20000
            run_simulation(cfg, should_upload)

