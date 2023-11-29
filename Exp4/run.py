from components.boards import HW2RISCVBoard
from components.processors import HW2MinorCPUStdCore, HW2FloatSIMDFU, HW2TimingSimpleCPU
from components.cache_hierarchies import HW2MESITwoLevelCache
from components.memories import HW2DDR3_1600_8x8

from workloads.daxpy_workload import DAXPYWorkload
from workloads.hello_world_workload import HelloWorkload
from workloads.roi_manager import exit_event_handler

from gem5.simulate.simulator import Simulator


import sys
from typing import Union
from pathlib import Path
from argparse import ArgumentParser

# ! Please replace the path to your gem5 python path
gem5_python_path = Path("/home/jack/opt/gem5/src/python")
if not gem5_python_path.exists or not gem5_python_path.is_dir():
    print(
        "Please replace the gem5_python_path in run.py to your gem5 installation path"
    )
    exit(1)
sys.path.append(str(gem5_python_path))


def simulation_step1(workload: Union[DAXPYWorkload, HelloWorkload]):
    memory: HW2DDR3_1600_8x8 = HW2DDR3_1600_8x8()
    cache: HW2MESITwoLevelCache = HW2MESITwoLevelCache()
    cpu: HW2TimingSimpleCPU = HW2TimingSimpleCPU()
    board = HW2RISCVBoard(
        clk_freq="4GHz",
        processor=cpu,
        memory=memory,
        cache_hierarchy=cache
    )
    board.set_workload(workload)
    simulator = Simulator(board=board, full_system=False, on_exit_event=exit_event_handler)
    simulator.run()
    print(
        "Simulation Finsihed\n"
        "======================================\n"
    )


def simulation_step2(workload: Union[HelloWorkload, DAXPYWorkload], issue_latency: int, fp_operation_latency: int):
    memory: HW2DDR3_1600_8x8 = HW2DDR3_1600_8x8()
    cache: HW2MESITwoLevelCache = HW2MESITwoLevelCache()
    cpu: HW2FloatSIMDFU = HW2FloatSIMDFU(operation_latency=fp_operation_latency, issue_latency=issue_latency)
    board = HW2RISCVBoard(
        clk_freq="4GHz",
        processor=cpu,
        memory=memory,
        cache_hierarchy=cache
    )
    board.set_workload(workload)
    simulator = Simulator(board=board, full_system=False, on_exit_event=exit_event_handler)
    simulator.run()
    print(
        "Simulation Finsihed\n"
        f"workload: {workload}\n"
        f"fp issue latency: {fp_operation_latency}\n"
        f"fp operation latency: {fp_operation_latency}\n"
        "======================================\n"
    )


def simulation_step3(workload: Union[HelloWorkload, DAXPYWorkload], int_operation_latency: int, fp_operation_latency: int):
    memory: HW2DDR3_1600_8x8 = HW2DDR3_1600_8x8()
    cache: HW2MESITwoLevelCache = HW2MESITwoLevelCache()
    cpu: HW2MinorCPUStdCore = HW2MinorCPUStdCore(
        int_issue_latency=1,
        int_operation_latency=int_operation_latency,
        fp_issue_latency=1,
        fp_operation_latency=fp_operation_latency
    )
    board = HW2RISCVBoard(
        clk_freq="4GHz",
        processor=cpu,
        memory=memory,
        cache_hierarchy=cache
    )
    board.set_workload(workload)
    simulator = Simulator(board=board, full_system=False, on_exit_event=exit_event_handler)
    simulator.run()
    print(
        "Simulation Finsihed\n"
        f"workload: {workload}\n"
        f"int issue latency: {int_operation_latency}\n"
        f"fp operation latency: {fp_operation_latency}\n"
        "======================================\n"
    )


def main():
    arg_parser = ArgumentParser(description="Simulator for Exp4")
    arg_parser.add_argument('-s', '--step', type=int,
                            help="Which step of Epx4")
    arg_parser.add_argument('-w', '--workload', type=str, help="Which workload to use")
    arg_parser.add_argument('-fi', '--fp_issue_latency', type=int,
                            help="What fp issue latency to use")
    arg_parser.add_argument('-fo', '--fp_operation_latency', type=int,
                            help="What fp operation latency to use")
    arg_parser.add_argument('-ii', '--int_issue_latency', type=int,
                            help="What int issue latency to use")
    arg_parser.add_argument('-io', '--int_operation_latency', type=int,
                            help="What fp operation latency to use")
    args = arg_parser.parse_args()

    assert args.step in [1, 2, 3], "Step should be 1, 2 or 3"
    workload: Union[HelloWorkload, DAXPYWorkload] = HelloWorkload() if args.workload == "HelloWorld" else DAXPYWorkload()
    if args.step == 1:
        simulation_step1(workload=workload)
    elif args.step == 2:
        simulation_step2(workload=workload, issue_latency=args.issue_latency, fp_operation_latency=args.fp_operation_latency)
    else:
        simulation_step3(workload=workload, int_operation_latency=args.int_operation_latency, fp_operation_latency=args.fp_operation_latency)


if __name__ == "__m5_main__":
    main()
