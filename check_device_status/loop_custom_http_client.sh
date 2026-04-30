#!/bin/bash

for i in $(seq 1 1000); do
    echo "Run $i of 1000"

    pids=()
    for j in $(seq 1 20); do
        pytest test_features_sim_increase_retry.py --log-cli-level=DEBUG -s &
        pids+=("$!")
    done

    failed=0
    for pid in "${pids[@]}"; do
        wait "$pid" || failed=1
    done

    if [ "$failed" -ne 0 ]; then
        echo "One or more parallel pytest runs failed in loop $i"
    fi
done
