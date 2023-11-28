#! /bin/env bash

exp=Exp2
dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# 复制workload
mkdir -p ~/.cache/gem5 && cp "${dir}"/${exp}/riscv-hello ~/.cache/gem5
# 切换assign
cd "${dir}"/gem5-assignment-template && git checkout assign-0
# 复制脚本
cp "${dir}"/${exp}/run.py "${dir}"/gem5-assignment-template

# 运行
gem5.opt "${dir}"/gem5-assignment-template/run.py

# 打包
tar czvf "${dir}"/${exp}.tar.gz -C "${dir}"/${exp} .
