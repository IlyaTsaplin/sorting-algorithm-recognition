import requests
from pathlib import Path


def load_step_solutions(step_id, token, data_directory):
    """
    Loads Python code solutions from given Stepik step to directory
    :param step_id: step id
    :param token: Stepik authentication token
    :param data_directory: path to directory where code solutions will be saved
    :return:
    """

    data_directory.mkdir(exist_ok=True)
    has_next = True
    step_directory = None
    while has_next:
        request_reply = requests.get('https://stepik.org/api/submissions',
                                     headers={'Authorization': 'Bearer ' + token},
                                     params={'step': step_id, 'status': 'correct'}
                                     ).json()
        has_next = request_reply['meta']['has_next']
        submissions = request_reply['submissions']

        for submission in submissions:
            code = submission['reply'].get('code', None)
            language = submission['reply'].get('language', None)
            if code is not None and language == 'python3':
                if not step_directory:
                    step_directory = data_directory / str(step_id)
                    step_directory.mkdir(exist_ok=True)
                with open(step_directory / f'{submission["id"]}.py', 'w') as file:
                    file.write(code)


def main():
    # Get your keys at https://stepik.org/oauth2/applications/
    # (client type = confidential, authorization grant type = client credentials)
    CLIENT_ID = "CLIENT_ID"
    CLIENT_SECRET = "CLIENT_SECRET"

    # Get a token
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.post('https://stepik.org/oauth2/token/',
                             data={'grant_type': 'client_credentials'},
                             auth=auth)
    token = response.json().get('access_token', None)
    if not token:
        print('Unable to authorize with provided credentials')
        exit(1)

    # Step_id list
    STEP_ID_LIST = []
    # Path to saved data directory
    PATH = Path('./data')

    for step_id in STEP_ID_LIST:
        load_step_solutions(step_id, token, PATH)


if __name__ == '__main__':
    main()
