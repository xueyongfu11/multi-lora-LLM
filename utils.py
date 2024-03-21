import json


def read_json_list(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f.readlines()]


def read_json_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_data(path, json_data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
