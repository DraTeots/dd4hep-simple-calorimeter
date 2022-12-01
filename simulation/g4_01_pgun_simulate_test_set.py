from g4_pgun_simulation import *

if __name__ == "__main__":

    should_upload = False

    for energy_gev in range(1, 11):
        for glass_type in ["PWO-CRYTUR", "PWO-SICCAS", "PWO-BOGO", "PWO-SICCAS-YANG", "CSGlass-0-T", "SciGlass-4-1-L", "SciGlass-4-1-T", "SciGlass-2-2-T", "SciGlass-2-1-L", "SciGlass-2-1-T", "SciGlass-1-1-T"]:

            # 1 electron
            cfg = G4SimConfig()
            cfg.executable = '/home/romanov/eic/kak-bog-cherepahu/cmake-build-debug/glass-prototype/cherepaha'
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

