import json

import requests

url = "http://192.168.1.19:8080/jsonrpc"

cookies_string = None


def auther():
    global cookies_string
    if cookies_string is None:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "login",
            "params": {"user": "admin", "passwd": "admin"}
        }
        auth = requests.post(url, json=payload, verify=False)
        cookies_string = auth.cookies
    return cookies_string


def get_th_id():
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "new_trans",
        "params": {"db": "running", "mode": "read"}
    }
    req = requests.post(url, cookies=auther(), json=payload, verify=False)
    response = req.text
    th_id = json.loads(response)["result"]["th"]

    return th_id


def transaction_info():
    get_th_id()
    payload = {
        "jsonrpc": "2.0",
        "id": 11,
        "method": "get_trans"
    }
    response = requests.post(url, cookies=auther(), json=payload, verify=False)
    st_response = response.text
    x = json.loads(st_response)["result"]["trans"][0]["db"]
    return x


def values():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_list_keys",
        "params": {"th": 1, "path": "/aaa/authentication/users/user"}
    }
    paylo = requests.post(url, cookies=auther(), json=payload, verify=False)
    return paylo.text


def specific_value():
    get_th_id()
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_values",
        "params": {
            "th": get_th_id(),
            "path": "/aaa/authentication/users/user{admin}",
            "leafs": ["uid", "gid", "password", "ssh_keydir", "homedir"]
        }
    }
    response = requests.post(url, cookies=auther(), json=payload, verify=False)
    return response.text


def syncer():
    get_th_id()
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "run_action",
        "params": {"th": 1, "path": "/devices/sync-from"}
    }
    response = requests.post(url, cookies=auther(), json=payload, verify=False)
    return response.text


print(transaction_info())
print(values())
print(specific_value())
print(syncer())