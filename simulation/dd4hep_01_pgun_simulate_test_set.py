from dd4hep_pgun_simulation import *
import os

os.environ["LD_LIBRARY_PATH"]="/home/romanov/eic/kak-bog-cherepahu/build/dd4hep/lib:" + os.environ["LD_LIBRARY_PATH"]
os.environ["DETECTOR_PATH"] = "/home/romanov/eic/kak-bog-cherepahu/dd4hep"

def sumulate_uniform_energy():
    should_upload = False

    # 1 electron
    cfg = SimConfig()
    cfg.e_max = 10
    cfg.detector_config = "wall_only"
    cfg.particle = "e-"
    cfg.events_num = 100
    run_simulation(cfg, should_upload)

    cfg.events_num = 1000
    run_simulation(cfg, should_upload)

    cfg.events_num = 10000
    run_simulation(cfg, should_upload)

    # 1 pion
    cfg.particle = "pi-"
    cfg.events_num = 100
    run_simulation(cfg, should_upload)

    cfg.events_num = 1000
    run_simulation(cfg, should_upload)

    cfg.events_num = 10000
    run_simulation(cfg, should_upload)

    # Now simulate large files
    cfg.particle = "e-"
    cfg.events_num = 100000
    run_simulation(cfg, should_upload)

    cfg.particle = "pi-"
    cfg.events_num = 100000
    run_simulation(cfg, should_upload)



if __name__ == "__main__":

    should_upload = False

    for energy_gev in [0.7, 1, 2, 3, 5, 10]:
        # 1 electron
        cfg = SimConfig()
        #cfg.executable = '/home/romanov/eic/kak-bog-cherepahu/glass-prototype/cmake-build-debug/cherepaha'        
        cfg.output_dir = "/mnt/work/data/epi"
        cfg.particle = "e-"
        cfg.e_max = energy_gev
        cfg.e_min = energy_gev
        cfg.detector_config = "wall_only"
        cfg.events_num = 20000
        run_simulation(cfg, should_upload)

        # 1 pion
        cfg.particle = "pi-"
        cfg.events_num = 20000
        run_simulation(cfg, should_upload)
