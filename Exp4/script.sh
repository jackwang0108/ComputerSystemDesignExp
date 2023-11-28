#! /bin/env bash

exp=Exp4
dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# 切换assign
cd "${dir}"/gem5-assignment-template && git checkout assign-2
# 复制脚本
cp "${dir}"/"${exp}"/run.py "${dir}"/gem5-assignment-template
# 复制workload
mkdir -p ~/.cache/gem5 && cp "${dir}"/${exp}/riscv-hello ~/.cache/gem5

# 运行

# Step 1
rm "${dir}"/"${exp}"/Step1.txt
workloads=("DAXPYWorkload" "HelloWorkload")
for workload in "${workloads[@]}"; do
    rm -f ~/.cache/gem5/riscv-hello.lock.lock
    gem5.opt "${dir}"/gem5-assignment-template/run.py -s 1 -w "${workload}"
    echo "Workload: ${workload}" >>"${dir}"/${exp}/Step1.txt
    grep 'commitStats0\.\(numFpInsts\|numIntInsts\|numLoadInsts\|numStoreInsts\)' "${dir}"/gem5-assignment-template/m5out/stats.txt >>"${dir}"/${exp}/Step1.txt
    printf "\n" >>"${dir}"/"${exp}"/Step1.txt
done

# Step 2
rm "${dir}"/"${exp}"/Step2.txt
fp_latencies=("3,2" "2,3" "6,1")
for latency in "${fp_latencies[@]}"; do
    IFS="," read -r fp_issue_latency fp_operation_latency <<<"$latency"
    for workload in "${workloads[@]}"; do
        gem5.opt "${dir}"/gem5-assignment-template/run.py -s 1 -w "${workload}" -fi "${fp_issue_latency}" -fo "${fp_operation_latency}"
        echo "Workload: ${workload}, fp_issue_latency: ${fp_issue_latency}, fp_operation_latency: ${fp_operation_latency}" >>"${dir}"/${exp}/Step2.txt
        grep 'commitStats0\.\(numFpInsts\|numIntInsts\|numLoadInsts\|numStoreInsts\)' "${dir}"/gem5-assignment-template/m5out/stats.txt >>"${dir}"/${exp}/Step2.txt
        printf "\n" >>"${dir}"/"${exp}"/Step2.txt
    done
    printf "\n\n\n" >>"${dir}"/"${exp}"/Step2.txt
done

# Step 3
rm "${dir}"/"${exp}"/Step3.txt
fp_latencies=("4,8" "2,8" "4,4")
for latency in "${fp_latencies[@]}"; do
    IFS="," read -r int_operation_latency fp_operation_latency <<<"$latency"
    for workload in "${workloads[@]}"; do
        gem5.opt "${dir}"/gem5-assignment-template/run.py -s 1 -w "${workload}" -io "${int_operation_latency}" -fo "${fp_operation_latency}"
        echo "Workload: ${workload}, int_operation_latency: ${int_operation_latency}, fp_operation_latency: ${fp_operation_latency}" >>"${dir}"/${exp}/Step3.txt
        grep 'commitStats0\.\(numFpInsts\|numIntInsts\|numLoadInsts\|numStoreInsts\)' "${dir}"/gem5-assignment-template/m5out/stats.txt >>"${dir}"/${exp}/Step3.txt
        printf "\n" >>"${dir}"/"${exp}"/Step3.txt
    done
    printf "\n\n\n" >>"${dir}"/"${exp}"/Step3.txt
done

# 打包
# tar czvf "${dir}"/Exp3.tar.gz -C "${dir}"/Exp3 .
