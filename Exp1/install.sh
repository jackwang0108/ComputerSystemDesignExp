#! /bin/env bash

dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# 下载依赖
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev python3-dev python-is-python3 libboost-all-dev pkg-config
# 下载Gem5
git clone https://github.com/gem5/gem5 "${dir}"/gem5
# 下载Python依赖
python -m pip install -r "${dir}"/gem5/requirements.txt
# 修改编译目标
sed -i "s/PROTOCOL = 'MI_example'/PROTOCOL = 'MESI_Two_Level'/g" "${dir}"/gem5/build_opts/RISCV
# 编译
cd "${dir}"/gem5 && scons build/RISCV/gem5.opt -j "$(nproc)"

# 添加环境变量
gem5_path="${dir}"/gem5/build/RISCV/
config=""
if [[ $SHELL == *"bash"* ]]; then
    config=~/.bashrc
elif [[ $SHELL == *"zsh"* ]]; then
    config=~/.zshrc
else
    echo "不支持的Shell: $SHELL"
    echo "请手动将 ${gem5_path}添加到PATH环境变量中"
fi
# shellcheck disable=SC2016
echo 'export PATH="${PATH}":'"${gem5_path}" >>"${config}"
echo "别忘了运行 source ${config}"
