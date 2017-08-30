#!/bin/bash
set -e
set -o pipefail

MARIAN_PATH=/mnt/disk/marian
MODEL_NAME=baseline

cat corpus.test.en \
   |  $MARIAN_PATH/build/amun \
        -c $MODEL_NAME.npz.amun.yml -b 12 -n --mini-batch 10 --maxi-batch 100 2>/dev/null \
   | $MARIAN_PATH/examples/training/moses-scripts/scripts/generic/multi-bleu.perl corpus.test.pt