#!/bin/bash -f

#install_vpr.sh

#This script installs VPR and genfasm when executed in the root directory of a
#VPR repository clone

make vpr -j$(nproc) && \
    make genfasm -j$(nproc)
