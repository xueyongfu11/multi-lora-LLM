from typing import List
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--IP", type=str, default="0.0.0.0")
parser.add_argument("--PORT", type=int, default=None)
parser.add_argument("--logging_level", type=str, default="info")
parser.add_argument("--load_all_lora", type=bool, default=True)
parser.add_argument("--load_just_one_lora", type=str, default=False)
parser.add_argument("--task_name", type=str, default=None)
parser.add_argument("--lora_path", type=str, default=None)
parser.add_argument("--logfile", type=str, default=None)
parser.add_argument("--base_model", type=str, default=None)
parser.add_argument("--gpus", type=List, default=None)
parser.add_argument("--use_qlora", type=bool, default=None)
parser.add_argument("--pipline", type=bool, default=None)
parser.add_argument("--origin_llm", type=bool, default=None)
parser.add_argument("--max_new_tokens", type=int, default=100)

args = parser.parse_args()
