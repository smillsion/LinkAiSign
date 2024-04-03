import os
import requests
import json

'''
cron: 15 3 * * *
new Env("LinkAi签到")
'''


def make_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}


def get_data(endpoint, token):
    headers = {
        'Accept': '*/*',
        'Authorization': f'Bearer {token}',
        'Referer': 'https://link-ai.tech/console/account',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    response_data = make_request(f'https://link-ai.tech/api/chat/web/app/user/{endpoint}', headers)
    data = response_data.get('data', {})
    score = data.get('score', -1) if data else -1
    success = response_data.get('success', '')
    return score, success, response_data


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


if __name__ == '__main__':
    token = os.getenv("LinkAiToken")
    if not token:
        print('LinkAiToken is null')
        exit()

    sign_score, sign_success, sign_response = get_data('sign/in', token)
    balance_score, balance_success, balance_response = get_data('get/balance', token)

    if not sign_success:
        message = sign_response.get('message', '')
        if sign_response.get('code', '') == 401:
            message = 'Token错误或失效'
        elif balance_success:
            message += f'\n当前积分【{balance_score}】'
        print(f'签到失败: {message}')
        mt_bark_server = os.getenv("MT_BARK_SERVER")
        mt_bark_key = os.getenv("MT_BARK_KEY")
        if mt_bark_server and mt_bark_key:
            push_msg(mt_bark_server, mt_bark_key, message)
    else:
        message = f'\n当前积分【{balance_score}】' if balance_success else ''
        print(f'签到成功: 获得积分【{sign_score}】{message}')
