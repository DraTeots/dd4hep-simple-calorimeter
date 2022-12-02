import subprocess
import datetime
import os


class G4SimConfig:

    def __init__(self):
        self.executable = 'cherepaha'
        self.events_num = 2000
        self.particle = "e-"
        self.energy = 1   # [GeV]
        self.multiplicity = 1
        self.file_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.output_dir = ""
        self.crystal_type = "SciGlass-4-1-L"
        self.crystal_size = 400


    @property
    def macro_file_name(self):
        file_name = f'{self.file_date}_g4_pgun_{self.crystal_type}_{self.particle}_e{self.energy}-GeV_{self.multiplicity}prt_{self.events_num}evt.mac'
        if self.output_dir:
            file_name = os.path.join(self.output_dir, file_name)
        return file_name

    @property
    def macro_content(self):
        return f"""
            # Set verbose level 
            /control/verbose 2
            /run/verbose 1
            /tracking/verbose 0

            # Set physics list (
            # 1st parameter - list name (FTFP_BERT, QGSP_BERT, QGSC_BERT_EMZ, ...)
            # 2nd parameter - use "withOptical" to turn on optical physics 
            /physics/selectList FTFP_BERT

            # Crystal size along X, Y and Z axis
            /detector/setCrystalSize 20 20 {self.crystal_size} mm

            # Crystal material - currently supported values are:
            # PWO-CRYTUR, PWO-SICCAS, PWO-BOGO, PWO-SICCAS-YANG
            # CSGlass-0-T, SciGlass-4-1-L, SciGlass-4-1-T, SciGlass-2-2-T, SciGlass-2-1-L, SciGlass-2-1-T, SciGlass-1-1-T 
            /detector/setCrystalMaterial {self.crystal_type}

            # Number of crystals in the assembly along X and Y axis
            /detector/setCrystalNumberX 13
            /detector/setCrystalNumberY 13

            # Wrap material. "C10H8O4" is vm2000. "G4_TEFLON" is teflon. "NONE" is no wrap material
            /detector/setWrapMaterial C10H8O4

            /detector/usePrimitiveScorer true
            /detector/saveEnergyWorldEscape false
            /detector/useGlobalScoringMeshes  false
            /detector/useUnitVolumeScoringMeshes false

            # Detector name                      Diameter   Glass type              Cathode
            # "R4125"    or "R1450"              18 mm      borosilicate default    bialkali
            # "R1828-01" or "H1949-51"           53 mm      borosilicate            bialkali
            # "R2059"    or "H3177"              53 mm      quartz (fused silica)   bialkali
            # "R2257"                            52 mm      borosilicate            multialkali
            # "S13360-6025CS" 6mm MPPC           6x6 mm     silicone resin          silicon crystal
            # "S13360-6025CS-2x2" 2x2 MPPC       12x12 mm   silicone resin          silicon crystal
            # "S13360-6025CS-20" 20mm MPPC       20x20 mm   silicone resin          silicon crystal
            # "S13360-6025CS-Custom" 2x2 MPPC    20x20 mm   silicone resin          silicon crystal
            #  with S14420-3025MG efficiency 
            /detector/setDetectorType R4125

            # Reflective shield (mostly important for MPPT, default is false)
            /detector/setReflectiveShield false

            # Set grease type (BC630 or PDMS) 
            /detector/setGreaseType BC630

            # Set grease thickness (use 0 for no grease) 
            /detector/setGreaseThickness 0 mm

            #/process/optical/verbose 10
            
            # Control optical processes
            #/process/optical/processActivation Cerenkov      true
            #/process/optical/processActivation OpAbsorption  false
            #/process/optical/processActivation OpBoundary    true
            #/process/optical/processActivation Scintillation true
            #/process/optical/processActivation OpRayleigh    false
            #/process/optical/processActivation OpMieHG       false
            #/process/optical/processActivation OpWLS         false
            
            #/process/optical/scintillation/setExcitationRatio .5
            #/process/optical/scintillation/setByParticleType false
            #/process/optical/scintillation/setTrackInfo      false
            #/process/optical/scintillation/setFiniteRiseTime false
            #/process/optical/scintillation/setStackPhotons   false
            
            #/process/optical/cerenkov/setMaxPhotons 3
            #/process/optical/cerenkov/setMaxBetaChange 10

            # Starting with Geant4 version 10.7, it is possible to specify up to three decay time constants, for particle-independent and particle-dependent yields
            #/process/optical/scintillation/setEnhancedTimeConstants true
            #/process/optical/scintillation/setByParticleType false
            #/process/optical/scintillation/setTrackInfo      false
            #/process/optical/scintillation/setFiniteRiseTime true
            #/process/optical/scintillation/setStackPhotons   true

            /run/initialize
            
            /geometry/test/run
            
            # /process/list
            
            # Particle gun (default)
            /gps/pos/type Point
            /gps/particle {self.particle}
            /gps/direction 0 0 1
            /gps/pos/centre 0 0 -40 mm
            
            # Particle gun (OP, SciGlass4 emission)
            # /control/execute macros/gps-sciglass-emission.mac
            # /control/execute macros/gps-pwo-emission.mac
            
            /gps/ene/mono {self.energy} GeV
            /gps/pos/centre 0. 0. -40. mm
            
              
            # 1000 optical photons, 10000 times
            /run/beamOn {self.events_num}
        """

    @property
    def sim_command_list(self):
        """Command to run simulation as a list of ddsim+flags"""
        sim_command = [
            f'{self.executable}',
            f'{self.macro_file_name}',
        ]
        return sim_command

    @property
    def sim_command(self):
        """Command to run simulation in one line"""
        return " ".join(self.sim_command_list)



def run_simulation(config: G4SimConfig, upload=False):
    """Runs simulation based on SimConfig and upload resulting data to S3 (if you have an access and flag is set)"""

    start_time = datetime.datetime.now()
    print(f"Simulation start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Simulation Command:\n    {config.sim_command}")

    with open(config.macro_file_name, 'w') as macro_file:
        macro_file.write(config.macro_content)

    # run! run! upload!
    subprocess.run(config.sim_command, shell=True, check=True, cwd=config.output_dir)

    # reporting end
    end_time = datetime.datetime.now()
    print(f"Simulation ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}, duration {end_time - start_time}: ")


if __name__ == "__main__":
    # 1 electron
    cfg = G4SimConfig()
    cfg.multiplicity = 1
    cfg.particle = "pi-"
    # cfg.events_num = 10
    # run_simulation(cfg, should_upload)
    #
    # cfg.events_num = 100
    # run_simulation(cfg, should_upload)
    cfg.detector_config = "wall_only"


    cfg.events_num = 100000
    run_simulation(cfg)

    # NOW ELECTRONS
    cfg.particle = "e-"
    run_simulation(cfg)
