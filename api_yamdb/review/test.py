import requests

origin = 'http://127.0.0.1:8000'

title_id = response.json()['id']

response = requests.get(
    f'{origin}/api/v1/pass-holders/{pass_holder_id}/',
    headers={'Authorization': f'Token {token}'},
)
print(response.status_code, response.text)