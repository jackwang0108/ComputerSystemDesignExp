# 实验二: 创建基本gem5配置脚本并运行

## 1. 说明

**实验二是后续实验的基础, 这个实验完成了从系统搭建, 仿真, 以及测试 (benchmarking)的一整个流程.**

通常我们为了直观的体会一个计算机系统的性能的, 在现实中我们会在真实的硬件上运行同一个程序, 通过观察程序运行的时间以直观的感受计算机系统的性能.

**`Gem5`也是按照同样的愿意进行的测试, 只不过相比于我们真实的去购买硬、搭建主机, `Gem5`所有的步骤都是使用软件模拟的.**

具体来说, 实验二的流程如下:

1. 首先搭建一个基础的计算机系统, 具有以下的配置: 
    
    - 处理器: `TimingSimpleCPU`
    - 缓存: `MESITwoLevelCache`
    - 内存: `DDR3_1600_8x8`
    - 主板: `RISCVBoard`

2. 而后为主板设置工作负载, 用于测试我们搭建出的计算机系统的性能.

    - 在实验二中, 工作负载就是运行一个`Hello World`程序

3. 启动模拟器, 按照设定的配置(在`run.py`中)模拟出一个计算机系统, 运行工作负载, 并将统计结果保存到`m5out/stats.txt`文件中

4. 完成模拟后, 通过观察`m5out`文件夹观察系统的性能.


因此, 完成实验二, 你将会明白计算机系统中的每一个实验是如何完成的, 以及未来真实的科研是如何进行的.


## 2. 使用


### 1. By Yourself

```bash
cd <path-to-project>/gem5-assignment-template
# 编写你的配置文件, 配置出你的计算机系统和仿真设置
code run.py
# 运行仿真
gem5.opt <path-to-project>/gem5-assignment-template/run.py
# 观察结果
vim <path-to-project>/gem5-assignment-template/m5out/stats.txt
```

### 2. My Example

并不是所有同学都有足够的能力在短时间内学懂`Gem5`, 因此我提供了`run.py`作为参考.

你也可以运行`script.sh`一键化运行得到结果. 但是还是推荐你自己按照流程做一遍实验, 因为计算机硬件层面的科研就是如此.

```bash
cd <path-to-project>
bash Exp2/scripts.sh
```
