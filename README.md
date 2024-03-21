# Multi-lora-LLM

## feature

- 支持高并发请求，将请求batch之后推理

- 在线支持不同任务训练的lora推理

- 快速添加常见大模型，目前base_model只支持qwen系列模型

## file explain

- scripts
  - 服务启动的脚本、压测脚本

- common_config.py
  - 配置lora 路径
  
- base_model.py
  - 大模型推理代码
  
- async_server.py
  - 支持多lora的并发服务
  
- tests
  - 测试相关代码
  


