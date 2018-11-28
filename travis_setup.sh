#!/usr/bin/env bash

# Just to be sure
pip install -U pip
# pip is not able to install distribute: "ImportError: No module named _markerlib"
easy_install distribute

pip install -U coverage
pip install coveralls
