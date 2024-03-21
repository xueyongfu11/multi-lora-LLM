import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

lora_prefix_dir = '##root_path##'
_lora2path = [
    ['lora1', 'path1'],
    ['lora2', 'path2'],
]

lora2path = [(item[0], os.path.join(lora_prefix_dir, item[1])) for item in _lora2path]

# 获取不同的任务类型
lora_tasks = [item[0] for item in lora2path]
origin_llm_tasks = []


