#!/usr/bin/env bash

python -m coverage run client/test.py
python -m coverage combine
python -m coverage report -m 2>&1
