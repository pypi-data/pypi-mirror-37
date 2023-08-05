import os
import requests
import json

if os.environ.get('API_URL') is None:
    API_URL = "https://api.acrosure.com"
else:
    API_URL = os.environ.get('API_URL')

def api( path, body = None, token = None):
    try:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        response = requests.post(API_URL + path,
            data = json.dumps(body),
            headers = headers)
        data = response.json()
        return data
    except Exception as err:
        error = err.args[0] 
        if hasattr(error, "get"):
            if error.get("response", {}).get("data"):
                raise Exception(error["response"]["data"])
            elif error.get("response"):
                raise Exception(error["response"])
        raise Exception(error)