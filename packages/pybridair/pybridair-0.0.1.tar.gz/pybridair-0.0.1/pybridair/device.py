
import requests, json
from pybridair.conn import check_response
from pybridair.data import *


def get_device_info(auth):
    base_url = "http://" + str(auth.ipaddress)
    data_url = "/info"
    data = pybridair.conn.get_data(auth, base_url, data_url)
    return data


def set_device_mode(auth, mode):
    modes = {"off" : 0,
             'smart' : 1,
             'auto' : 2,
             'boost' : 3,
             'night' : 4}
    base_url = "http://" + str(auth.ipaddress)
    data_url = "/settings"
    f_url = base_url+data_url
    data = {"mode" : modes[mode]}
    response = requests.post(f_url, headers=auth.headers, json=data)
    check_response(response)
    return json.loads(response.text)


def get_device_mode(auth):
    status = get_status(auth)
    modes = {
        "off": 0,
        'smart': 1,
        'auto': 2,
        'boost': 3,
        'night': 4
    }
    for k,v in modes.items():
        if status['Settings']['Mode'] == v:
            return k






