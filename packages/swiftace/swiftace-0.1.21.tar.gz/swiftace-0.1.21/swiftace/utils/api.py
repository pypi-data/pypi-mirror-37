"""API requests and backend communication utilities"""
import os
import requests
import time
from tusclient import client
from tusclient.storage import filestorage
from swiftace.utils import credentials
from io import StringIO

# API_URL = 'https://swiftai-217215.appspot.com'
API_URL = "https://api.swiftace.ai"


def make_tus_client():
    credentials.create_config_dir()
    return {
        'client': client.TusClient(f'{API_URL}/uploads/'),
        'storage_file': filestorage.FileStorage(credentials.CONFIG_DIR/'.tus-storage-file'),
        'chunk_size': 2*1024*1024  # 2 MB
    }


tus = make_tus_client()


class ApiError(Exception):
    """Error class for web API related Exceptions"""
    pass


def validate_api_key(api_key):
    """Validate the API key by making a request to server"""
    res = requests.get(
        f'{API_URL}/user/profile',
        headers={'Authorization': f'Bearer {api_key}'})
    if res.status_code == 200:
        return True
    elif res.status_code == 401:
        return False
    raise ApiError(f'Something went wrong: f{res.text}')


def get_api_key():
    """Retrieve the API Key (from memory, credentials file or user input)"""
    if not credentials.api_key_exists():
        api_key, write = credentials.read_or_ask_api_key()
        if not validate_api_key(api_key):
            print('[swiftace] Error: The API key provided is invalid or expired.')
            api_key = credentials.ask_api_key()
            write = True
            if not validate_api_key(api_key):
                raise ApiError(
                    'Error: The API key provided is invalid or expired.')
        credentials.write_api_key(api_key, write)
    return credentials.CREDS['API_KEY']


def get_auth_header():
    return {"Authorization": f"Bearer {get_api_key()}"}


def upload_conda_env(data, name):
    """Upload the anaconda environment to server"""
    files = {'env': ('environment.yml', data)}
    res = requests.post(f'{API_URL}/environment', files=files,
                        data={'name': name}, headers=get_auth_header())
    if res.status_code == 200:
        res_json = res.json()
        env_hash = res_json['hash']
        return env_hash
    else:
        raise ApiError(f'Evironment upload failed! {res.content}')


def download_conda_env(env_id):
    """Download an anaconda environment to a string"""
    res = requests.get(f'{API_URL}/environment/{env_id}')
    if res.status_code == 200:
        return res.content
    else:
        raise ApiError(f'Environment download failed! {res.content}')


def create_project(slug):
    """Upload the anaconda environment to server"""
    res = requests.post(f'{API_URL}/project',
                        data={'slug': slug}, headers=get_auth_header())
    if res.status_code == 200:
        res_json = res.json()
        slug = res_json['slug']
        return slug
    else:
        raise ApiError(f'Project init failed! {res.content}')


def create_experiment_run(project_slug, name="", desc=""):
    """Upload the anaconda environment to server"""
    res = requests.post(f'{API_URL}/experiment',
                        data={'project': project_slug,
                              'name': name, 'desc': desc},
                        headers=get_auth_header())
    if res.status_code == 200:
        res_json = res.json()
        experiment_hash = res_json['hash']
        return experiment_hash
    else:
        raise ApiError(f'Project init failed! {res.content}')


def timestamp_ms():
    """Return the current timestamp (in milliseconds)"""
    return int(time.time() * 1000)


def post_block(run_id, block, data_type):
    """Upload metrics, hyperparameters and other information to server"""
    url = f'{API_URL}/data/{run_id}/hyperparams'
    data = [{"local_ts": timestamp_ms(), "block": block,
             'record_type': data_type}]
    res = requests.post(url, json=data, headers=get_auth_header())
    if res.status_code == 200:
        return res.json()
    else:
        raise ApiError(f'Data logging failed! {res.content}')


def upload_env_file(run_id, env_str, name):
    meta = {'name': name}
    tus_client = tus['client']
    tus_client.set_headers(get_auth_header())
    uploader = tus_client.uploader(
        file_stream=StringIO(env_str), chunk_size=tus['chunk_size'],
        metadata=meta, store_url=True, url_storage=tus['storage_file'])
    uploader.upload()
    file_url = uploader.url
    file_id = file_url.split('/')[-1]

    url = f'{API_URL}/experiment/{run_id}/files'
    data = {
        "env": {"files": []},
        "source": {"files": []},
        "other": {"files": []},
    }
    data["env"]["files"].append(file_id)
    res = requests.post(url, json=data, headers=get_auth_header())
    if res.status_code == 200:
        return file_id
    else:
        raise ApiError(f'File upload failed! {res.content}')


def upload_file(run_id, path, typ='other'):
    """Upload a file (supports chunking and resumable uploads)"""
    if not os.path.exists(path):
        raise FileNotFoundError(f'No such file or directory: {path}')
    tus_client = tus['client']
    tus_client.set_headers(get_auth_header())
    meta = {'filename': path.split('/')[-1], 'local_path': path}
    uploader = tus_client.uploader(path, chunk_size=tus['chunk_size'],
                                   metadata=meta, store_url=True,
                                   url_storage=tus['storage_file'])
    uploader.upload()
    file_url = uploader.url
    file_id = file_url.split('/')[-1]

    url = f'{API_URL}/experiment/{run_id}/files'
    data = {
        "env": {"files": []},
        "source": {"files": []},
        "other": {"files": []},
    }
    data[typ]["files"].append(file_id)
    res = requests.post(url, json=data, headers=get_auth_header())
    if res.status_code == 200:
        return file_id
    else:
        raise ApiError(f'File upload failed! {res.content}')


def post_commit(run_id, data):
    """Create a commit for the given run_id"""
    url = f'{API_URL}/experiment/{run_id}/commit'
    res = requests.post(url, json=data, headers=get_auth_header())
    if res.status_code == 200:
        return res.json()
    else:
        raise ApiError(f'Commit failed! {res.content}')
