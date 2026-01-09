#!/bin/bash

fetch() {
    wget https://cdn.intra.42.fr/document/document/35238/npuzzle-gen.py
}

venv() {
    uv sync
    echo "To activate the venv run : source .venv/bin/activate"
}

usage() {
    cmds=$(declare -F | awk '{print $3}' | paste -s -d'|' -)
    echo "Usage: ./make.sh [$cmds]"
}

# ENTRY POINT

cmd="$1"

if [[ -z "$cmd" || "$cmd" == "help" ]]; then
    usage
    exit 0
fi

# Check if function exists, then call
if declare -F "$cmd" > /dev/null; then
    "$cmd"
else
    echo "Unknown command: $cmd"
    echo
    usage
    exit 1
fi