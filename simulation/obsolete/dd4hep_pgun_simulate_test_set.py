from dd4hep_pgun_simulation import *

if __name__ == "__main__":

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
