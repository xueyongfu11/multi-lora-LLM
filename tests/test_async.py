# import requests
# import json
#
# url = "http://127.0.0.1:38094/async/has_goal"
#
# # 准备你的POST请求的数据
# data = {
#     "content": '你是谁'
# }
#
# # 将数据转换为JSON格式
# json_data = json.dumps(data)
#
# # 发送POST请求
# response = requests.post(url, headers={"Content-Type": "application/json"}, data=json_data)
#
# # 打印响应
# print("状态码:", response.status_code)
# print("响应体:", response.json())

import requests
import json
import time
import concurrent.futures

url = "http://127.0.0.1:38094/async/has_goal"

sample = {
    "traceId": "fc2b5b0b-026a-4910-870f-0922a7e66d30",
    "sessionId": "02b88907-5bc1-4eec-bc81-c4d1e5095bad",
    "userId": "02b88907-5bc1-4eec-bc81-c4d1e5095bad",
    "sendTime": 1705648755553,
    "stream": False,
    "dialogueHistory": [{
        "queryInfo": {
            "semanticQueryList": [
                "你好"
            ],
            "rawQueryObjList": [
                "你好"
            ]
        },
        "responseInfo": {
            "response": "你好"
        }
    }
    ],
    "queryInfo": {
        "semanticQueryList": [
            "都是我的错"
        ],
        "rawQueryObjList": [
            "你好"
        ]
    }
}

# 准备并发请求的数据列表
data_list = [sample] * 50


# 定义一个函数来发送单个POST请求
def send_post_request(data):
    json_data = json.dumps(data)
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json_data)
    return response

cur_time = time.time()
res = []
# 使用ThreadPoolExecutor来并发地发送请求
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # 你可以调整max_workers的数量
    future_to_url = {executor.submit(send_post_request, data): data for data in data_list}
    for future in concurrent.futures.as_completed(future_to_url):
        data = future_to_url[future]
        res.append(data)
        try:
            # 获取请求的结果
            response = future.result()
            # 打印结果
            print(f"Data: {data}, 状态码: {response.status_code}, 响应体: {response.json()}")
        except Exception as exc:
            print(f'生成请求 {data} 时出错: {exc}')
print(f'cost time: {time.time() - cur_time}')