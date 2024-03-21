#!/bin/bash

cd ../server

base_model=/root/models/Qwen1.5-7B-Chat

# test
CUDA_VISIBLE_DEVICES=7 python async_server.py \
  --PORT 38094 \
  --logging_level info \
  --load_all_lora true \
  --logfile logs/async/process1_log.txt \
  --base_model ${base_model} \
  --max_new_tokens 5


