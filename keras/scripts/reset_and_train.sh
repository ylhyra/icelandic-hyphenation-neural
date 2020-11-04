#!/bin/bash
cd "$(dirname "$0")"
cd ..

rm -f data/best_model.h5
rm -f data/models_latest.h5
rm -f data/models.h5

python3 train.py
