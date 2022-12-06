import subprocess
import datetime
import os

os.environ["DETECTOR_PATH"] = "/home/romanov/eic/kak-bog-cherepahu/dd4hep"
os.environ["LD_LIBRARY_PATH"] = "/home/romanov/eic/kak-bog-cherepahu/build/dd4hep/lib:" + os.environ.get("LD_LIBRARY_PATH", "")

class SimConfig:

    def __init__(self):
        self.events_num = 2000
        self.particle = "e-"
        self.e_min = 0.01   # [GeV]
        self.e_max = 30     # [GeV]
        self.multiplicity = 1
        self.detector_config = "epic_arches"
        self.template_xml = "wall_only_template.xml"
        self.file_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.template_xml = ""
        self.output_dir = ""
        self.module_width = "20*mm"
        self.module_length = "400*mm"
        self.module_material = "SciGlass"   # SciGlass or PbWO4
        self.output_file_tag = "pgun_SciGlass-2x2x40"

    @property
    def output_base_file_name(self):
        return f'{self.output_dir}/{self.file_date}_{self.output_file_tag}_{self.particle}_{self.detector_config}_e{self.e_min}-{self.e_max}GeV_center_{self.multiplicity}prt_{self.events_num}evt'

    @property
    def output_file_name(self):
        return f'{self.output_base_file_name}.edm4hep.root'

    @property
    def output_gdml_file_name(self):
        return f'{self.output_base_file_name}.geometry.gdml'

    @property
    def output_dd4hep_xml_file_name(self):
        return f'{self.output_base_file_name}.xml'

    @property
    def sim_command_list(self):
        """Command to run simulation as a list of ddsim+flags"""
        sim_command = [
            f'ddsim',
            #f'--compactFile=$DETECTOR_PATH/{self.detector_config}.xml',
            f'--compactFile={self.output_dd4hep_xml_file_name}',
            f'-N={self.events_num}',
            f'--random.seed=1',
            f'--enableGun',
            f'--gun.particle="{self.particle}"',
            f'--gun.momentumMin={self.e_min}*GeV',
            f'--gun.momentumMax={self.e_max}*GeV',
            f'--gun.thetaMin=0*deg',
            f'--gun.thetaMax=0*deg',
            f'--gun.phiMin=0*deg',
            f'--gun.phiMax=0*deg',
            f'--gun.distribution=uniform',
            f'--outputFile={self.output_file_name}',
        ]
        return sim_command

    @property
    def gen_geo_command(self):
        """Command to generate geometry"""
        return f"geoConverter -compact2gdml -input $DETECTOR_PATH/{self.detector_config}.xml -output {self.output_gdml_file_name}"

    @property
    def sim_command(self):
        """Command to run simulation in one line"""
        return " ".join(self.sim_command_list)

def run_simulation(config: SimConfig):
    """Runs simulation based on SimConfig and upload resulting data to S3 (if you have an access and flag is set)"""

    start_time = datetime.datetime.now()
    print(f"Simulation start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Simulation Command:\n    {config.sim_command}")

    with open(config.template_xml, 'r') as template_file:
        template_content = template_file.read()
        template_content = template_content.replace("{{ModuleWidth}}", config.module_width)
        template_content = template_content.replace("{{ModuleLength}}", config.module_length)
        template_content = template_content.replace("{{ModuleMaterial}}", config.module_material)

    with open(config.output_dd4hep_xml_file_name, 'w') as macro_file:
        macro_file.write(template_content)

    # run! run! upload!
    subprocess.run(config.sim_command, shell=True, check=True)

    # reporting end
    end_time = datetime.datetime.now()
    print(f"Simulation ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}, duration {end_time - start_time}: ")


def gen_geometry(config: SimConfig):
    """Generates geometry in GDML file"""
    
    # gen! gen! gen!
    subprocess.run(config.gen_geo_command, shell=True, check=True)
    print(f"Saved geometry ast: {config.output_gdml_file_name}: ")


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


def simulate_fixed_energy():    
    for energy_gev in [0.7, 1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18]:
        for glass_type in ["PbWO4", "SciGlass"]:
            # 1 electron
            cfg = SimConfig()
            
            cfg.output_dir = "/mnt/work/data/epi/21x21"
            cfg.template_xml = os.environ["DETECTOR_PATH"] + "/wall_only_template.xml"
            cfg.particle = "e-"
            cfg.e_max = energy_gev
            cfg.e_min = energy_gev
            cfg.detector_config = "wall_only"
            cfg.events_num = 20000
            cfg.module_width="20*mm"
            cfg.module_length="400*mm" if glass_type.startswith("SciGlass") else "200*mm"
            cfg.module_material = glass_type
            cfg.output_file_tag = f"pgun_{glass_type}_2x2x" + ("40" if glass_type.startswith("SciGlass") else "20")
            run_simulation(cfg)

            # 1 pion
            cfg.particle = "pi-"
            cfg.events_num = 20000
            run_simulation(cfg)


if __name__ == "__main__":

    # should_upload = False

    # cfg = SimConfig()
    # cfg.output_dir = "/mnt/work/data/epi"
    # cfg.particle = "e-"
    # cfg.detector_config = "wall_only"
    # cfg.events_num = 20000
    # gen_geometry(cfg)
    simulate_fixed_energy()

