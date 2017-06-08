#!/bin/bash
cd '$HOME/git/miscellany'
tmux new-session -d
tmux split-window -h
tmux split-window -v '/$HOME/misc/bin/python3 /$HOME/git/miscellany/manage.py runserver'
tmux select-pane -t 0
tmux -2 attach-session -d
