NUM_SPAWNS=$1 
SESSION=$2
tmux new-session -s $SESSION -n bash -d
for ID in `seq 100 $NUM_SPAWNS`; 
do      
    tmux new-window -t $ID
    tmux send-keys -t $SESSION:$ID 'python /Users/samantha/Documents/GitHub/InsightDE-Waitless/Input/RI_4_fanout_shards.py' C-m
done
