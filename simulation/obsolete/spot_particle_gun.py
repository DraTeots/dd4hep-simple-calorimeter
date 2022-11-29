"""Runs pythia hepmc file through dd4hep simulation"""
import subprocess
from datetime import datetime

macro_file = "disk_particle_gun.mac"
events_num = 1000
output_file = f"spot_particle_gun_{events_num}.edm4hep.root"
detector_config = "wall_only"


import os

os.environ["DETECTOR_PATH"] = "/home/romanov/eic/kak-bog-cherepahu/"
os.environ["LD_LIBRARY_PATH"] = "/home/romanov/eic/kak-bog-cherepahu/cmake-build-debug/lib:" + os.environ["LD_LIBRARY_PATH"]

# npsim --compactFile=$DETECTOR_PATH/ecce.xml --runType=run --enableG4GPS --macro disk_particle_gun.mac --outputFile=/media/share/data/disk_gun_electrons_0-15GeV_100ev.edm4hep.root

sim_command = [
    f'ddsim',
    f'--compactFile=$DETECTOR_PATH/{detector_config}.xml',
    f'--runType=run',
#    f'-N {events_num}',
    f'--random.seed=1',
    f'--enableG4GPS',
#    f'--inputFiles {input_file}',
    f'--outputFile={output_file}',
]




start_time = datetime.now()
print(f"Simulation start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Simulation Command:\n    {sim_command}")

# run! run!
subprocess.run(" ".join(sim_command), shell=True, check=True)

# reporting end
end_time = datetime.now()
print(f"Simulation ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}, duration {end_time - start_time}: ")




# [filename](_media/example.js ':include :type=code :fragment=demo')