import os
import time
from pydantic import BaseModel, Field, UUID4
from typing import List
import traceback
import uvicorn
from fastapi import FastAPI, Depends
import sys

sys.path.append('..')

from config import common_config
from models.base_model import MultiLora
from logger import Logger
from models.service_streamer import Streamer  # ThreadedStreamer,
from args_parser import args

app = FastAPI()


class QueryInfo(BaseModel):
    semanticQueryList: List[str]
    rawQueryObjList: List[str]


class ResponseInfo(BaseModel):
    response: str


class DialogueHistory(BaseModel):
    queryInfo: QueryInfo
    responseInfo: ResponseInfo


class RequestData(BaseModel):
    traceId: UUID4
    sessionId: UUID4
    userId: UUID4
    sendTime: int
    stream: bool
    dialogueHistory: List[DialogueHistory]
    queryInfo: QueryInfo


class ResponseData(BaseModel):
    traceId: UUID4
    sessionId: UUID4
    userId: UUID4
    sendTime: int
    responseInfo: ResponseInfo


class BatchData(BaseModel):
    contents: List[str]


class BatchResponseData(BaseModel):
    model_pred: List[str]

@app.post("/native/{task_name}", response_model=ResponseData)
def task_predict(task_name: str, item: RequestData):
    logger.info(f'received request: task_name: {task_name}, request data: {item.dict()}')
    inputs = [item.queryInfo.semanticQueryList[0]]
    multi_lora_model.set_lora(task_name)
    response = multi_lora_model.predict(inputs)[0]
    response_data = {'traceId': item.traceId, 'sessionId': item.sessionId, 'userId': item.userId,
                     'sendTime': int(time.time() * 1000), 'responseInfo': {'response': response}}
    logger.info(f'response data: {response_data}')
    return response_data

# 当使用stream时，不能使用async关键词，否则无法使用并发
@app.post("/async/{task_name}", response_model=ResponseData)
def task_predict(task_name: str, item: RequestData):
    logger.info(f'received request: task_name: {task_name}, request data: {item.dict()}')
    inputs = [item.queryInfo.semanticQueryList[0]]
    response = streamer.predict(inputs, task_name)[0]
    response_data = {'traceId': item.traceId, 'sessionId': item.sessionId, 'userId': item.userId,
                     'sendTime': int(time.time() * 1000), 'responseInfo': {'response': response}}
    logger.info(f'response data: {response_data}')
    return response_data


if __name__ == '__main__':
    root_path = common_config.project_root
    logger = Logger(logfile=os.path.join(root_path, args.logfile),
                    logging_level=args.logging_level).logger

    # MultiLora不能输入common_config，因为common_config无法序列化，因为是个python模块
    multi_lora_model = MultiLora(args)

    streamer = Streamer(multi_lora_model, multi_lora_model.predict, batch_size=32, max_latency=0.3)

    uvicorn.run(app, host=args.IP, port=args.PORT)
