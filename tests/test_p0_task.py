import requests
import json
import time


# url = "http://127.0.0.1:38094/non_async/copying_type"
# url = "http://127.0.0.1:38094/async/has_goal"
# url = "http://127.0.0.1:6009/non_async/copying_type"
url = "https://u158554-a9b8-1ed74a47.westc.gpuhub.com:8443/non_async/has_goal"

cur_time = time.time()
for _ in range(2):
    # 准备你的POST请求的数据
    data = {
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
                "以下是一段对话\"心理咨询师：你好，很高兴为你提供咨询服务。近期有什么事情让你感到困扰吗？\n用户：我和我的伴侣最近老是吵架，我觉得我们沟通出了问题，但是又不知道怎么解决。\n心理咨询师：感情中的冲突很常见。你们是否尝试过坐下来平静地谈论彼此的感受和需求呢？有效的倾听和表达也很重要。\n用户：我们试过了，但总是说着说着就开始激动起来。我想知道怎样才能更好地控制情绪。\n心理咨询师：学习一些情绪管理技巧可能会有所帮助，例如深呼吸、正念冥想或是进行身心锻炼。当感觉到自己要失控时，暂停并给自己几分钟冷静的时间也是个好方法。\"，请识别用户的回答\"{用户：听起来很有道理，我会试试的。哦，对了，你会弹吉他吗？}\"是否包括\"我不知道\"语义，包括返回\"是\"，不包括返回\"否\"。只返回\"是\"或者\"否\"。\"我不知道\"的定义是，对咨询师的提问，用户没有办法，没有想法。"
            ],
            "rawQueryObjList": [
                "以下是一段对话\"心理咨询师：你好，很高兴为你提供咨询服务。近期有什么事情让你感到困扰吗？\n用户：我和我的伴侣最近老是吵架，我觉得我们沟通出了问题，但是又不知道怎么解决。\n心理咨询师：感情中的冲突很常见。你们是否尝试过坐下来平静地谈论彼此的感受和需求呢？有效的倾听和表达也很重要。\n用户：我们试过了，但总是说着说着就开始激动起来。我想知道怎样才能更好地控制情绪。\n心理咨询师：学习一些情绪管理技巧可能会有所帮助，例如深呼吸、正念冥想或是进行身心锻炼。当感觉到自己要失控时，暂停并给自己几分钟冷静的时间也是个好方法。\"，请识别用户的回答\"{用户：听起来很有道理，我会试试的。哦，对了，你会弹吉他吗？}\"是否包括\"我不知道\"语义，包括返回\"是\"，不包括返回\"否\"。只返回\"是\"或者\"否\"。\"我不知道\"的定义是，对咨询师的提问，用户没有办法，没有想法。"
            ]
        }
    }

    # 将数据转换为JSON格式
    json_data = json.dumps(data)

    # 发送POST请求
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json_data)

    # 打印响应
    print("状态码:", response.status_code)
    print("响应体:", response.json())
print((time.time() - cur_time) / 50)


# import requests
# import json
# import concurrent.futures
# import time
#
# url = "https://u158554-a9b8-1ed74a47.westc.gpuhub.com:8443/non_async/has_goal"
#
# sample = {
#     "traceId": "fc2b5b0b-026a-4910-870f-0922a7e66d30",
#     "sessionId": "02b88907-5bc1-4eec-bc81-c4d1e5095bad",
#     "userId": "02b88907-5bc1-4eec-bc81-c4d1e5095bad",
#     "sendTime": 1705648755553,
#     "stream": False,
#     "dialogueHistory": [{
#         "queryInfo": {
#             "semanticQueryList": [
#                 "你好"
#             ],
#             "rawQueryObjList": [
#                 "你好"
#             ]
#         },
#         "responseInfo": {
#             "response": "你好"
#         }
#     }
#     ],
#     "queryInfo": {
#         "semanticQueryList": [
#             "都是我的错" * 200
#         ],
#         "rawQueryObjList": [
#             "你好"
#         ]
#     }
# }
#
# # 准备并发请求的数据列表
# data_list = [sample] * 30
#
#
# # 定义一个函数来发送单个POST请求
# def send_post_request(data):
#     json_data = json.dumps(data)
#     response = requests.post(url, headers={"Content-Type": "application/json"}, data=json_data)
#     return response
#
#
# # 使用ThreadPoolExecutor来并发地发送请求
# cur_time = time.time()
# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # 你可以调整max_workers的数量
#     future_to_url = {executor.submit(send_post_request, data): data for data in data_list}
#     for future in concurrent.futures.as_completed(future_to_url):
#         data = future_to_url[future]
#         try:
#             # 获取请求的结果
#             response = future.result()
#             # 打印结果
#             print(f"Data: {data}, 状态码: {response.status_code}, 响应体: {response.json()}")
#         except Exception as exc:
#             print(f'生成请求 {data} 时出错: {exc}')
# print((time.time() - cur_time) / 30)
