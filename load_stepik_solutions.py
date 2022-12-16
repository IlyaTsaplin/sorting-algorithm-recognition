import requests
import json

# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)
client_id = "yuuCGclGQnTQE6LpAT1vRExkJej0N4O5X4TAJrfm"
client_secret = "OCy4aDfhqTjWbWIhUYeu3PnirhfTar3Lh20zH4aRDJEsW3IfouWbJSNO5ebHIc4agGmAu8jq32ZZ4Tl5o29jTh28TnrWvzcOLgV0wAzU4FgkKNvaWPF5405ykKtNshCb"

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)

# 3. Call API (https://stepik.org/api/docs/) using this token.
api_url = 'https://stepik.org/api/submissions'
step_id = 3555515
path = './data/'

solution_counter = 0
has_next = True
while has_next:
    request_reply = requests.get(api_url,
                                 headers={'Authorization': 'Bearer ' + token},
                                 params={'step': step_id, 'status': 'correct'}
                                 ).json()
    has_next = request_reply['meta']['has_next']
    submissions = request_reply['submissions']

    for submission in submissions:
        code = submission['reply'].get('code', None)
        language = submission['reply'].get('language', None)
        if code is not None and language == 'python3':
            solution_counter += 1
            with open(path + f'{step_id}_{solution_counter}.py', 'w') as file:
                file.write(code)
