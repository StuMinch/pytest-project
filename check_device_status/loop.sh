#!/bin/bash

for i in $(seq 1 100); do
    echo "Run $i of 100"
    pytest test_features_sim.py --log-cli-level=DEBUG -s
done
