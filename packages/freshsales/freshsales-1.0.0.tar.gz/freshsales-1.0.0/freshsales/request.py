from .freshsales_exception import FreshsalesException
import requests
import json

def _request(path, payload):
    try:
        data = json.dumps(payload)
        headers = { 'content-type': 'application/json', 'accept': 'application/json' }
        resp = requests.post(path, data=data, headers=headers)
        if resp.status_code != 200:
            raise  FreshsalesException("Freshsales responded with the status code of %s" % str(resp.status_code))
    except requests.exceptions.RequestException as e:
        raise FreshsalesException(e.message)
