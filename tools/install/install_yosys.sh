#!/bin/bash -f

#install_yosys.sh

#This script installs Yosys and when executed in the root directory of a
#Yosys repository clone

make config-gcc && \
    make -j$(nproc)
