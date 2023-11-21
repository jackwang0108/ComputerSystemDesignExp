# 实验一: Gem5简介及环境配置

实验一首先对Gem5进行了介绍, 而后配置环境

运行`install.sh`一键化安装. 注意, 由于网络问题可能导致下载失败, 请开启代理后运行如下命令为Git添加代理
```bash
git config --global https.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890
```
注意把端口`7890`修改为你的代理软件监听的端口

此外, 编译大概会花费30分钟左右, 内存占用大概6G左右
