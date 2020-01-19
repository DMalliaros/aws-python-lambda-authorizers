import json
from http import HTTPStatus

import requests


def get_jwks(issuer_url):
    keys_url = issuer_url + '/.well-known/jwks.json'
    response_cognito = requests.get(keys_url)

    if response_cognito.status_code != HTTPStatus.OK:
        raise Exception('Http request to cognito jwks url: {} failed'.format(keys_url))

    response_json = json.loads(response_cognito.text)['keys']
    response = dict()
    for i in range(len(response_json)):
        response[response_json[i]['kid']] = response_json[i]

    return response
