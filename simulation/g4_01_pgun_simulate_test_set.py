#!/usr/bin/env python3

from g4_pgun_simulation import *

if __name__ == "__main__":

    should_upload = False

    for energy_gev in [0.7, 1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18]:
        for glass_type in ["PWO-CRYTUR", "SciGlass-4-1-LB"]:

            # 1 electron
            cfg = G4SimConfig()
            cfg.executable = '/home/romanov/eic/kak-bog-cherepahu/build/glass-prototype/cherepaha'
            cfg.energy = energy_gev
            cfg.output_dir = "/mnt/work/data/epi/21x21"
            cfg.particle = "e-"
            cfg.crystal_type = glass_type
            cfg.crystal_size = 400 if glass_type.startswith("SciGlass") else 200
            cfg.events_num = 20000
            run_simulation(cfg, should_upload)

            # 1 pion
            cfg.particle = "pi-"
            cfg.events_num = 20000
            run_simulation(cfg, should_upload)

