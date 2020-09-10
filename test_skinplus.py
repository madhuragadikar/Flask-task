import requests
import json


def test_signup():
    url = 'http://127.0.0.1:5000/signup'

    # Additional headers.
    headers = {'Content-Type': 'application/json' }

    # Body
    payload = {'email': 'xxx@xxx.com'}

    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    print(resp.text)


def test_finish():
    url = 'http://127.0.0.1:5000/finish'

    # Additional headers.
    headers = {'Content-Type': 'application/json' }

    # Body
    payload = {'email': 'xxx@xxx.com'}
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    print(resp.text)


def test_update_survey():
    url = 'http://127.0.0.1:5000/survey/2'

    # Additional headers.
    headers = {'Content-Type': 'application/json' }

    # Body
    payload = {"name": "medicines",
               "is_pregnant_nursing_conceiving": "true"}

    # convert dict to json by json.dumps() for body data.
    resp = requests.put(url, headers=headers, data=json.dumps(payload,indent=4))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200