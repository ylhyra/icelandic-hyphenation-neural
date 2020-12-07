#!/bin/bash
cd "$(dirname "$0")"
cd ..

rm -f models/model_best.h5
rm -f models/models_latest.h5
rm -f models/model_saved.h5

python3 train.py
