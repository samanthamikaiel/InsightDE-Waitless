NUM_SPAWNS=$1
SESSION=$2
tmux new-session -s $SESSION -n bash -d
for ID in `seq 1 $NUM_SPAWNS`;
do
    tmux new-window -t $ID
    tmux send-keys -t $SESSION:$ID 'python /Users/samantha/Documents/GitHub/InsightDE-Waitless/Input/RI_1shard.py' C-m
done
