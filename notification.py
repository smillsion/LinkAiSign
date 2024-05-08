import requests
import json


def push_msg(server, key, msg):
    try:
        payload = {
            "body": msg,
            "device_key": key,
            "title": f"LinkAi签到失败",
            "badge": 1
        }
        requests.post(
            url=f"{server}/push",
            headers={"Content-Type": "application/json; charset=utf-8"},
            data=json.dumps(payload)
        )
    except requests.exceptions.RequestException as e:
        print(f'HTTP Request failed: {e}')
