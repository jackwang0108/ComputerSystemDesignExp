# 实验一: Gem5简介及环境配置

## 1. 说明

**实验一首先对`Gem5`进行了介绍, 而后编译安装`Gem5`.**

`Gem5`是一个广泛使用的计算机系统模拟器, 用于研究和开发计算机体系结构, 微处理器设计, 内存系统, 缓存系统和其他相关领域. `Gem5`可以模拟多种处理器架构, 包括x86, ARM, RISC-V等.

**在计算机系统综合实验中, 我们会使用`Gem5`模拟一个计算机系统, 并运行工作负载(通常是一个`C/C++`程序), 来探究不同的系统架构对计算机系统性能的影响.为此, 我们需要首先编译, 安装`Gem5`.**

第一次实验, 即`实验一`(`Exp1`)的目标就是编译, 安装 `Gem5`. 你当然可以跟随实验课堂上的教学一步一步安装`Gem5`, 也可以跟随这里的指导一步步安装.

**注意: `Gem5`编译过程会使用到`Python`, 而`Anaconda`管理的`Python`和系统中的`Python`会发生冲突, 因此在安装前请确保运行`conda deactivate`退出所有`Conda Python`环境.**



## 2. 使用

注意, 安装过程中需要从`Github`下载仓库. 因此由于网络问题可能导致下载失败, 请开启代理软件后运行如下命令为Git添加代理
```bash
git config --global https.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890
```
注意把端口`7890`修改为你的代理软件监听的端口

**此外, 编译大概会花费30分钟左右, 内存占用大概6G左右, 如果你开的虚拟机内存较小, 或者你的物理机器内存较小, 请增加交换分区的大小, 以顺利编译**

### 方法A: 懒人方法

我提供了一个脚本一键化编译, 安装`Gem5`:

```bash
bash Exp1/install.sh
```
脚本并不确保跨平台性, 不过好在并不复杂, 因此因为你的`CPU`指令集架构导致无法成功运行脚本, 请你检查下脚本在运行.

### 方法B: 手动安装

首先下载系统依赖和`Python`依赖
```bash
# 安装系统依赖
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev python3-dev python-is-python3 libboost-all-dev pkg-config
# 安装Python依赖
python -m pip install -r "${dir}"/gem5/requirements.txt
```

然后修改编译目标. 将`<path-to-project>/gem5/build_opts/RISCV`文件中下述行
```bash
PROTOCOL = 'MI_example'
```
修改为
```bash
PROTOCOL = 'MESI_Two_Level'
```

然后利用`scons`进行编译, **编译过程大概30分钟左右**
```bash
scons build/RISCV/gem5.opt -j "$(nproc)"
```

编译完成后, 将编译得到的`gem5`可执行文件路径添加到`PATH`环境变量中. 注意替换`<path-to-project>`为实际路径, `config`替换为你的`Shell`的配置文件
```bash
config=~/.zshrc
gem5_path=<path-to-project>/gem5/build/RISCV/
echo 'export PATH="${PATH}":'"${gem5_path}" >>"${config}"
```


### 使用Gem5
安装完`Gem5`后, 重新加载`Shell`配置文件即可使用
```bash
source ~/.zshrc
# 或者
source ~/.bashrc
```

运行`gem5.opt`即可运行`Gem5`
![成功使用Gem5](assets/gem5.png)