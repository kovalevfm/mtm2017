#!/bin/bash
set -e
set -o pipefail

MARIAN_PATH=/mnt/disk/marian
MODEL_NAME=baseline

$MARIAN_PATH/build/marian \
        --model $MODEL_NAME.npz \
        --devices 0 --seed 0 \
        --train-sets corpus.train.en corpus.train.pt \
        --vocabs vocab.en.yml vocab.pt.yml \
        --dim-vocabs 66000 50000 \
        --dynamic-batching -w 3000 \
        --layer-normalization --dropout-rnn 0.2 --dropout-src 0.1 --dropout-trg 0.1 \
        --early-stopping 5 --moving-average \
        --valid-freq 10000 --save-freq 10000 --disp-freq 1000 \
        --valid-sets corpus.valid.en corpus.valid.en \
        --valid-metrics cross-entropy valid-script \
        --valid-script-path ./valid.sh \
        --log train.log --valid-log valid.log