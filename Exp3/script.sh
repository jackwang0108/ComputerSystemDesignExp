#! /bin/env bash

exp=Exp3
dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# 切换assign
cd "${dir}"/gem5-assignment-template && git checkout assign-1
# 复制脚本
cp "${dir}"/"${exp}"/run.py "${dir}"/gem5-assignment-template

# 运行

# Step 1
rm "${dir}"/"${exp}"/Step1.txt
for freq in 1 2 4; do
    cpus=("simple" "minor")
    for cpu in "${cpus[@]}"; do
        gem5.opt "${dir}"/gem5-assignment-template/run.py -s 1 -c "${cpu}" -m 1600 -f $freq -n 224 >>"${dir}"/"${exp}"/Step1.txt
    done
done

# Step 2
rm "${dir}"/"${exp}"/Step2.txt
memorys=("1600" "2133" "LPDDR3")
for memory in "${memorys[@]}"; do
    cpus=("simple" "minor")
    for cpu in "${cpus[@]}"; do
        gem5.opt "${dir}"/gem5-assignment-template/run.py -s 2 -c "${cpu}" -m "${memory}" -f 1 -n 224 >>"${dir}"/"${exp}"/Step2.txt
    done
done

# 打包
tar czvf "${dir}"/"${exp}".tar.gz -C "${dir}"/${exp} .
