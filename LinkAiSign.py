import datetime
import os
import random
import time

import requests
import base64
import json

'''
cron: 15 3 * * *
new Env("LinkAi签到")
'''

def sign(token):
    headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' + token,
        'Referer': 'https://link-ai.tech/console/account',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    response = requests.get(
        'https://link-ai.tech/api/chat/web/app/user/sign/in', headers=headers)
    json_data = response.json()
    data = json_data.get('data', {})
    score = data.get('score', -1) if data else -1
    code = json_data.get('code', '')
    message = json_data.get('message', '')
    return score, code, message

if __name__ == '__main__':
    token = os.getenv("LinkAiToken")
    # mt_version = os.getenv("Mt_Version")
    if not token:
        print('LinkAiToken is null')
        exit()
    # mt_bark_server = os.getenv("MT_BARK_SERVER")
    # mt_bark_key = os.getenv("MT_BARK_KEY")
    # server_check = False;
    # key_check = False;
    score, code, message = sign(token)
    if code != '200':
        print('fail: ' + message)
    else:
        print('success: ' + score)