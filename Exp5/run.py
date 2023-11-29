from components.boards import HW3RISCVBoard
from components.processors import HW3O3CPU
from components.cache_hierarchies import HW3MESICache
from components.memories import HW3DDR4

from workloads.bubble_sort_workload import BubbleSortWorkload
from workloads.bfs_workload import BFSWorkload
from workloads.matmul_workload import MatMulWorkload

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


class HW3BigCore(HW3O3CPU):
    def __init__(self, width=12, rob_size=352, num_int_regs=280, num_fp_regs=224):
        super().__init__(width, rob_size, num_int_regs, num_fp_regs)


class HW3SmallCore(HW3O3CPU):
    def __init__(self, width=4, rob_size=152, num_int_regs=100, num_fp_regs=84):
        super().__init__(width, rob_size, num_int_regs, num_fp_regs)


class HW3MediumCore(HW3O3CPU):
    def __init__(
        self,
        width: int = 4,
        rob_size: int = 152,
        num_int_regs: int = 100,
        num_fp_regs: int = 84,
    ):
        super().__init__(width, rob_size, num_int_regs, num_fp_regs)


def simulation_step1(
    cpu: Union[HW3BigCore, HW3SmallCore],
    workload: Union[BFSWorkload, MatMulWorkload, BubbleSortWorkload],
):
    memory: HW3DDR4 = HW3DDR4()
    cache: HW3MESICache = HW3MESICache()
    board = HW3RISCVBoard(
        clk_freq="2GHz", processor=cpu, memory=memory, cache_hierarchy=cache
    )
    board.set_workload(workload)
    simulator = Simulator(board=board, full_system=False)
    simulator.run()
    print(
        "Simulation Finsihed\n"
        f"CPU: {cpu}\n"
        f"Workload: {workload}\n"
        "======================================\n"
    )


def simulation_step2(
    cpu: HW3MediumCore, workload: Union[BFSWorkload, MatMulWorkload, BubbleSortWorkload]
):
    memory: HW3DDR4 = HW3DDR4()
    cache: HW3MESICache = HW3MESICache()
    board = HW3RISCVBoard(
        clk_freq="2GHz", processor=cpu, memory=memory, cache_hierarchy=cache
    )
    board.set_workload(workload)
    simulator = Simulator(board=board, full_system=False)
    simulator.run()
    with Path(__file__).resolve().parent.parent.joinpath("Exp5/Step2.txt").open(
        mode="a"
    ) as f:
        f.write(
            f"CPU: {cpu}\n"
            f"width: {cpu._width}\n"
            f"rob_size: {cpu._rob_size}\n"
            f"num_int_regs: {cpu._num_int_regs}\n"
            f"num_fp_regs: {cpu._num_fp_regs}\n"
            f"score: {cpu.get_area_score()}\n"
            f"workload: {workload}\n"
        )
    print(
        "Simulation Finsihed\n"
        f"CPU: {cpu}\n"
        f"workload: {workload}\n"
        "======================================\n"
    )


def main():
    arg_parser = ArgumentParser(description="Simulator for Exp5")
    arg_parser.add_argument("-s", "--step", type=int, help="Which step of Epx5")
    arg_parser.add_argument("-w", "--workload", type=str, help="Which workload to use")
    arg_parser.add_argument("-c", "--cpu", type=str, help="Which cpu to use")
    arg_parser.add_argument("-wd", "--width", type=int, help="What width to use")
    arg_parser.add_argument("-r", "--rob_size", type=int, help="What rob size to use")
    arg_parser.add_argument(
        "-ni", "--num_int_reg", type=int, help="How many int registers to use"
    )
    arg_parser.add_argument(
        "-nf", "--num_fp_reg", type=int, help="How many float registers to use"
    )
    args = arg_parser.parse_args()

    assert args.step in [1, 2], "Step should be 1, 2"
    workload: Union[MatMulWorkload, BubbleSortWorkload, BFSWorkload]
    if args.workload == "bfs":
        workload = BFSWorkload()
    elif args.workload == "bubble":
        workload = BubbleSortWorkload()
    else:
        workload = MatMulWorkload()

    cpu: Union[HW3BigCore, HW3SmallCore, HW3MediumCore]
    if args.cpu == "small":
        cpu = HW3SmallCore()
    elif args.cpu == "big":
        cpu = HW3BigCore()
    else:
        cpu = HW3MediumCore(
            width=args.width,
            rob_size=args.rob_size,
            num_int_regs=args.num_int_reg,
            num_fp_regs=args.num_fp_reg,
        )
    if args.step == 1:
        simulation_step1(workload=workload, cpu=cpu)
    else:
        simulation_step2(workload=workload, cpu=cpu)


if __name__ == "__m5_main__":
    main()
