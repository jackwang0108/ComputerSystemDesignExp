#! /bin/env bash

exp=Exp5
dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# 切换assign
cd "${dir}"/gem5-assignment-template && git checkout assign-3
# 复制脚本
cp "${dir}"/"${exp}"/run.py "${dir}"/gem5-assignment-template

# 运行

# Step 1
# rm "${dir}"/"${exp}"/Step1.txt
workloads=("bfs" "bubble" "matmul")
# for workload in "${workloads[@]}"; do
#     cpus=("big" "small")
#     for cpu in "${cpus[@]}"; do
#         gem5.opt "${dir}"/gem5-assignment-template/run.py -s 1 -c "${cpu}" -w "${workload}"
#         echo "CPU: $cpu, Workload: ${workload}" >>"${dir}"/${exp}/Step1.txt
#         grep 'cores\.core\.\(ipc\|numCycles\)' "${dir}"/gem5-assignment-template/m5out/stats.txt >>"${dir}"/${exp}/Step1.txt
#         printf "\n" >>"${dir}"/"${exp}"/Step1.txt
#     done
#     printf "\n\n\n" >>"${dir}"/"${exp}"/Step1.txt
# done

# # Step 2
rm -f "${dir}"/"${exp}"/Step2.txt
cpu="medium"
for workload in "${workloads[@]}"; do
    for width in {4..12..4}; do
        for rob_size in {152..352..50}; do
            for num_int_reg in {100..280..60}; do
                for num_fp_reg in {84..224..70}; do
                    gem5.opt "${dir}"/gem5-assignment-template/run.py -s 2 -c "${cpu}" -w "${workload}" -wd "${width}" -r "${rob_size}" -ni "${num_int_reg}" -nf "${num_fp_reg}"
                    echo "CPU: ${cpu}, width: ${width}, rob_size: ${rob_size}, num_int_reg: ${num_int_reg}, num_fp_reg: ${num_fp_reg}, Workload: ${workload}" >>"${dir}"/${exp}/Step2.txt
                    grep 'cores\.core\.\(ipc\|numCycles\)' "${dir}"/gem5-assignment-template/m5out/stats.txt >>"${dir}"/${exp}/Step2.txt
                    printf "\n" >>"${dir}"/"${exp}"/Step2.txt
                done
                printf "\n\n" >>"${dir}"/"${exp}"/Step2.txt
            done
            printf "\n\n\n\n" >>"${dir}"/"${exp}"/Step2.txt
        done
        printf "\n\n\n\n\n" >>"${dir}"/"${exp}"/Step2.txt
    done
    printf "\n\n\n\n\n\n\n" >>"${dir}"/"${exp}"/Step2.txt
done

# # 打包
# tar czvf "${dir}"/${exp}.tar.gz -C "${dir}"/${exp} .

# # 重置修改方便下个实验
# cd "${dir}"/gem5-assignment-template && git checkout -- componenets/cache_hierarchies.py
