#!/bin/bash
# Requirements: pip3 install tensorflowjs
cd "$(dirname "$0")"

tensorflowjs_converter --quantization_bytes 1 \
                       --input_format keras \
                       ./../keras/models/model_best.h5 \
                       ./../build/model/
# tensorflowjs_converter  --input_format keras \
#                       ./../keras/models/model_best.h5 \
#                       ./../build/model/
