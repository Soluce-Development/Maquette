import json


def get_datas(filename):
    file = './Datas/' + filename + '.json'
    with open(file, "r", encoding='utf-8') as f:
        datas = json.load(f)
        return datas


def update_data(filename, new_value: str):
    file = './Datas/' + filename + '.json'
    with open(file, "w", encoding='utf-8') as f:
        json.dump(new_value, f, indent=4)
