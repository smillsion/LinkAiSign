
import os
import requests
import json
from notification import push_msg

'''
cron: 15 3 * * *
new Env("LinkAi签到")
'''

def make_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
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
    return response_data


def login(username, password):
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    payload = {
        "username": username,
        "password": password
    }
    response_data = requests.post(
        url=f'https://link-ai.tech/api/login',
        headers=headers,
        data=payload
    )
    response = response_data.json()
    success = response.get('success', '')
    message = response.get('message')
    if success:
        new_token = response.get('data').get('token')
        # os.environ['LinkAiToken'] = new_token
        # 要修改的环境变量和新值
        set_env(new_token)
        return new_token, message
    return None, message


def set_env(link_ai_token):
    if os.path.exists("/ql/config/auth.json"):
        config = "/ql/config/auth.json"

    if os.path.exists("/ql/data/config/auth.json"):
        config = "/ql/data/config/auth.json"

    with open(config, "r", encoding="utf-8") as f1:
        ql_token = json.load(f1)['token']

    if ql_token != "":
        url = 'http://127.0.0.1:5600/api/envs'
        headers = {'Authorization': f'Bearer {ql_token}'}
        body = {
            'searchValue': 'LinkAiToken',
            'Authorization': f'Bearer {ql_token}'
        }
        datas = requests.get(url, params=body, headers=headers).json()['data']
        if datas:
            # 暂时只支持1个token
            data = datas[0]
            body = {"name": "LinkAiToken", "value": link_ai_token, "remarks": data['remarks'], "id": data['id']}
            # 更新
            requests.put(url, json=body, headers=headers)

            url = 'http://127.0.0.1:5600/api/envs/enable'
            body = [body['id']]
            # 启用
            requests.put(url, json=body, headers=headers)
            print(f"更新成功")
        else:
            body = [{"value": link_ai_token, "remarks": "LinkAi-Token", "name": "LinkAiToken"}]
            # 新增
            requests.post(url, json=body, headers=headers)
            print(f"新增成功")


if __name__ == '__main__':
    token = os.getenv("LinkAiToken")
    if not token:
        print('LinkAiToken is null')
        username = os.getenv("LA_USERNAME")
        password = os.getenv("LA_PASSWORD")
        if username and password:
            print(f'设置了用户名和密码，尝试登陆')
            login_result, login_message = login(username, password)
            if login_result:
                token = login_result
            else:
                print(f'❌❌❌重新登陆失败，' + login_message + '\n脚本执行结束')
                exit()
        else:
            exit()

    endpoints = ['sign/in', 'get/balance']
    results = [get_data(endpoint, token) for endpoint in endpoints]

    is_finally_fail = False
    is_retry_attempted = False  # 添加标志用于记录是否已尝试重新签到

    result = results[0]
    if not result.get('success', ''):
        is_finally_fail = True
        message = result.get('message', '')
        if result.get('code', '') == 401 and not is_retry_attempted:  # 检查是否是第一次签到失败且未尝试过重新签到
            is_retry_attempted = True  # 设置为已尝试重新签到
            message = 'Token错误或失效'
            username = os.getenv("LA_USERNAME")
            password = os.getenv("LA_PASSWORD")
            if username and password:
                print(message + f'\n设置了用户名和密码，尝试重新登陆')
                login_result, login_message = login(username, password)
                if login_result:
                    print(f'登陆成功：新token为：👇👇👇👇👇\n' + login_result)
                    print(f'重新执行签到')
                    results = [get_data(endpoint, login_result) for endpoint in endpoints]
                    message = results[0].get('message', '')
                    if not results[0].get('success', ''):
                        if results[0].get('code', '') == 401:
                            message = '新Token无法完成签到，请手动获取Token'
                        elif results[1].get('success', ''):
                            message += f'❌❌❌\n当前积分【{results[1].get("data", {}).get("score", -1)}】'
                    else:
                        message = f'✅✅✅\n当前积分【{results[1].get("data", {}).get("score", -1)}】' if results[1].get('success', '') else ''
                        print(f'✅✅✅签到成功: 获得积分【{results[0].get("data", {}).get("score", -1)}】{message}')
                        is_finally_fail = False
                else:
                    if login_message:
                        print(f'重新登陆失败，' + login_message)
                        message = message + f'❌❌❌\n尝试重新登陆失败，请检查用户名和密码，或手动获取Token'
                    else:
                        print(f'重新登陆失败，请手动登陆获取token后写入环境变量')
        elif results[1].get('success', ''):
            message += f'❌❌❌\n当前积分【{results[1].get("data", {}).get("score", -1)}】'

        if is_finally_fail:
            print(f'❌❌❌签到失败: {message}')
            mt_bark_server = os.getenv("MT_BARK_SERVER")
            mt_bark_key = os.getenv("MT_BARK_KEY")
            if mt_bark_server and mt_bark_key:
                push_msg(mt_bark_server, mt_bark_key, f'❌❌❌' + message)
    else:
        message = f'✅✅✅\n当前积分【{results[1].get("data", {}).get("score", -1)}】' if results[1].get('success', '') else ''
        print(f'✅✅✅签到成功: 获得积分【{results[0].get("data", {}).get("score", -1)}】{message}')
