from components.boards import HW1RISCVBoard
from components.processors import HW1MinorCPU, HW1TimingSimpleCPU
from components.cache_hierarchies import HW1MESITwoLevelCache
from components.memories import HW1DDR3_1600_8x8, HW1DDR3_2133_8x8, HW1LPDDR3_1600_1x32

from workloads.mat_mul_workload import MatMulWorkload

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


def simulation_step1(size: int, freq: int, cpu: Union[HW1TimingSimpleCPU, HW1MinorCPU]):
    """
    Runs a simulation of a matrix multiplication workload on a specific combination of CPU frequency and CPU type using the gem5 simulator.

    Args:
        size (int): The size of the matrix multiplication workload.
        freq (int): The CPU frequency in GHz. Only frequencies of 1, 2, or 4 are allowed for exp1.
        cpu: The CPU type. Only instances of HW1MinorCPU or HW1TimingSimpleCPU are allowed.

    Returns:
        None

    Raises:
        AssertionError: If the specified size is less than or equal to 1.
        AssertionError: If the specified frequency is not allowed for exp1.
        AssertionError: If the specified CPU type is not allowed.

    Examples:
        simulation_exp1(2, HW1TimingSimpleCPU())
    """
    assert 1 <= size, f"size should greater than 1: {size}"
    assert freq in {1, 2, 4}, f"Not allow freq for exp1: {freq}"
    assert isinstance(
        cpu, (HW1MinorCPU, HW1TimingSimpleCPU)
    ), f"Not allow CPU type: {type(cpu)}"

    memory = HW1DDR3_1600_8x8()
    cache = HW1MESITwoLevelCache()
    workload = MatMulWorkload(size)
    board = HW1RISCVBoard(
        clk_freq=f"{freq}GHz", processor=cpu, memory=memory, cache_hierarchy=cache
    )
    board.set_workload(workload)
    simulator = Simulator(board=board, full_system=False)

    simulator.run()
    print(
        f"CPU: {type(cpu)}\n"
        f"Freq: {freq}\n"
        f"Simulation Finished\n"
        f"===========================================================\n\n"
    )


def simulation2(
    size: int,
    cpu: Union[HW1TimingSimpleCPU, HW1MinorCPU],
    memory: Union[HW1DDR3_1600_8x8, HW1DDR3_2133_8x8, HW1LPDDR3_1600_1x32],
):
    """
    Runs a simulation of a matrix multiplication workload on a specific combination of CPU type and memory type using the gem5 simulator.

    Args:
        size (int): The size of the matrix multiplication workload.
        cpu: The CPU type. Only instances of HW1MinorCPU or HW1TimingSimpleCPU are allowed.
        memory: The memory type. Only instances of HW1DDR3_1600_8x8, HW1DDR3_2133_8x8, or HW1LPDDR3_1600_1x32 are allowed.

    Returns:
        None

    Raises:
        AssertionError: If the specified size is less than or equal to 1.
        AssertionError: If the specified CPU type is not allowed.
        AssertionError: If the specified memory type is not allowed.

    Examples:
        simulation2(224, HW1TimingSimpleCPU(), HW1DDR3_1600_8x8())
    """
    assert 1 <= size, f"size should greater than 1: {size}"
    assert isinstance(
        cpu, (HW1MinorCPU, HW1TimingSimpleCPU)
    ), f"Not allowed CPU type: {type(cpu)}"
    assert isinstance(
        memory, (HW1DDR3_1600_8x8, HW1DDR3_2133_8x8, HW1LPDDR3_1600_1x32)
    ), f"Now allowed memory: {type(memory)}"

    memory = HW1DDR3_1600_8x8()
    cache = HW1MESITwoLevelCache()
    workload = MatMulWorkload(size)
    board = HW1RISCVBoard(
        clk_freq="4GHz", processor=cpu, memory=memory, cache_hierarchy=cache
    )
    board.set_workload(workload)
    simulator = Simulator(board=board, full_system=False)

    simulator.run()
    print(
        f"CPU: {type(cpu)}\n"
        f"Memory: {type(memory)}\n"
        f"Simulation Finished\n"
        f"===========================================================\n\n"
    )


def main():
    arg_parser = ArgumentParser(description="Simulator for Exp3")
    arg_parser.add_argument("-s", "--step", type=int, help="Which step of epx3")
    arg_parser.add_argument("-c", "--cpu", type=str, help="Which cpu to use")
    arg_parser.add_argument("-f", "--freq", type=int, help="What frequency to use")
    arg_parser.add_argument(
        "-m",
        "--memory",
        type=str,
        default=HW1MESITwoLevelCache(),
        help="Which memory to use",
    )
    arg_parser.add_argument("-n", "--num", type=int, help="size of the matrix")
    args = arg_parser.parse_args()

    assert args.step in [1, 2], "Step should be 1 or 2"
    cpu = HW1TimingSimpleCPU() if args.cpu == "simple" else HW1MinorCPU()
    if args.step == 1:
        simulation_step1(size=args.num, freq=args.freq, cpu=cpu)
    else:
        if args.memory == "1600":
            memory = HW1DDR3_1600_8x8()
        elif args.memory == "2133":
            memory = HW1DDR3_2133_8x8()
        else:
            memory = HW1LPDDR3_1600_1x32()
        simulation2(size=args.num, cpu=cpu, memory=memory)


if __name__ == "__m5_main__":
    # simulation_step1(224, 1, HW1TimingSimpleCPU())
    main()
