#!/bin/bash

function create_venv {
    python3 -m venv civitaidl_env
    source civitaidl_env/bin/activate
    pip3 install -r requirements.txt
}

function run_civitaidl {
    python_name='python3'
    has_python3=$(type "python3")
    has_python=$(type "python")
    if [ $has_python3 = "python3 not found" ]; then
        echo "Python3 not found, trying python"
        python_name='python'
    elif [ $has_python = "python not found" ]; then
        echo "Python must be installed to run CivitAIDL"
        return 1
    fi
    $python_name main.py $@
}

if [ "$VIRTUAL_ENV" = "civitaidl_env" ]; then
    run_civitaidl $@
else
    if [ ! -d civitaidl_env ]; then
        create_venv
    fi
    run_civitaidl $@
fi