#!/bin/bash
# run by bash spawn_kafka_streams.sh <KAFKA_BROKER_PUBLIC_IP> <SESSION_NAME> <NUM_CARS>
IP_ADDR=$1
NUM_SPAWNS=1
SESSION=$2
NUM_CARS=$3
tmux new-session -s $SESSION -n bash -d
for ID in `seq 1 $NUM_SPAWNS`;
do
    echo $ID
    tmux new-window -t $ID
    tmux send-keys -t $SESSION:$ID 'python traffic_simulator.py '"$IP_ADDR"' '"$NUM_CARS"'' C-m
done
