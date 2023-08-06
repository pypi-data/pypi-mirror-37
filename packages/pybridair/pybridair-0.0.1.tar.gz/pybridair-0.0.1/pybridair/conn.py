import requests, json

def check_response(response):
    if response.status_code != 200:
        raise ConnectionError("No connection with the API. Status code {}".format(response.status_code))
    return

def get_data(auth, base_url, data_url, args=''):
    f_url= base_url + data_url + args
    response = requests.get(f_url, headers=auth.headers)
    check_response(response)
    return json.loads(response.text)

def set_data(auth, base_url, data_url, args=''):
    f_url= base_url + data_url + args
    response = requests.post(f_url, headers=auth.headers)
    check_response(response)
    return json.loads(response.text)