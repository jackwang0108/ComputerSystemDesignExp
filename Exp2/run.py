from components.boards import HW0RISCVBoard 
from components.processors import HW0TimingSimpleCPU 
from components.cache_hierarchies import HW0MESITwoLevelCache 
from components.memories import HW0DDR3_1600_8x8 
 
from workloads.hello_world_workload import HelloWorldWorkload 
 
from gem5.simulate.simulator import Simulator


import sys
from pathlib import Path
# ! Please replace the path to your gem5 python path
gem5_python_path = Path("/home/jack/opt/gem5/src/python")
if not gem5_python_path.exists or not gem5_python_path.is_dir():
    print("Please replace the gem5_python_path in run.py to your gem5 installation path")
    exit(1)
sys.path.append(str(gem5_python_path))
 
if __name__ == "__m5_main__": 
 
        cpu = HW0TimingSimpleCPU() 
        cache = HW0MESITwoLevelCache() 
        memory = HW0DDR3_1600_8x8() 
        board = HW0RISCVBoard( 
                clk_freq="2GHz", processor=cpu, cache_hierarchy=cache, memory=memory 
        ) 
        workload = HelloWorldWorkload() 
        board.set_workload(workload) 
        simulator = Simulator(board=board, full_system=False) 
        simulator.run() 
 
        print("Finished simulation.")