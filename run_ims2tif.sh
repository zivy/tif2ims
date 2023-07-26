#!/bin/bash

cd "$(dirname "$BASH_SOURCE")"
# provide the full path to the Anaconda/Miniconda
# installation.
PATH_TO_ANACONDA=/Users/yanivz/toolkits/anaconda3
"$PATH_TO_ANACONDA"/envs/tif2ims/bin/pythonw ims2tif.py
