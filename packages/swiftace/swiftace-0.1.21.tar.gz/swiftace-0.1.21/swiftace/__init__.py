import hashlib
from tqdm import tqdm_notebook
from time import sleep
from swiftace.utils import validate_project_name, api, init_experiment, linkify
from swiftace.utils.checksum import get_hash
from swiftace.utils.anaconda import save_conda_env
from swiftace.utils.jupyter import upload_notebook, set_notebook_name, get_notebook_name
from swiftace.utils.git import git_commit_push

# WEB_APP_URL = 'https://swiftai-217215.firebaseapp.com'
WEB_APP_URL = 'https://app.swiftace.ai'
current_proj = None
current_run_id = None

__all__ = ['init', 'log_dataset', 'log_hyperparams',
           'log_metrics', 'upload_file', 'commit']


def init(project_name):
    """Initialize a project and create a new session"""
    global current_run_id
    current_run_id = None
    init_project(project_name)
    new_session()
    set_notebook_name()


def init_project(name):
    """Initialize the given project"""
    global current_proj
    if current_proj is None or current_proj != name:
        validate_project_name(name)
        resp = api.create_project(name)
        if resp:
            current_proj = resp
    print(
        f'[swiftace] Initlalized project: "{current_proj}"')


def new_session(force=False, log=True):
    """Start a new session (run), if one doesn't exist"""
    global current_proj
    global current_run_id
    if current_run_id is None or force:
        resp = init_experiment(current_proj)
        if resp is not None:
            current_run_id = resp
    if log:
        print(f'[swiftace] Tracking experiment: "{current_run_id}"')


def get_run_id():
    if not current_proj or not current_run_id:
        raise Exception(
            "Please initialize a project using 'swiftace.init' before logging.")
    return current_run_id


def log_dataset(path, include_hash=True):
    """Record the dataset (file or directory)"""
    path = str(path)
    run_id = get_run_id()
    data = {'dataset': path}
    msg = f"[swiftace] Dataset logged: '{path}'"
    if include_hash:
        print('[swiftace] Computing checksum..')
        dataset_hash = get_hash(path)
        data['dataset_hash'] = dataset_hash
        msg += f"\n[swiftace] Checksum: {dataset_hash}"
    api.post_block(run_id, data, 'datasets')
    print(msg)


def log_hyperparams(data):
    """Record hyperparameters for the current experiment"""
    run_id = get_run_id()
    api.post_block(run_id, data, 'hyperparams')
    print('[swiftace] Hyperparameters logged.')


def log_metrics(data):
    """Record metrics for the current experiment"""
    run_id = get_run_id()
    api.post_block(run_id, data, 'metrics')
    print('[swiftace] Metrics logged.')


def upload_file(path):
    """Upload a file and link it to the curren experiment"""
    run_id = get_run_id()
    api.upload_file(run_id, path)
    print(f'[swiftace] File "{path}" uploaded.')


def commit(message, init_new_session=True):
    """Create a commit for the current experiment"""
    run_id = get_run_id()

    print('[swiftace] Capturing environment..')
    env_hash = save_conda_env(run_id)

    print('[swiftace] Saving Jupyter notebook...')
    notebook_id = upload_notebook(run_id)

    print('[swiftace] Creating git commit..')
    git_meta = git_commit_push(message)

    print('[swiftace] Finalizing commit...')
    data = {'env': env_hash, 'code': notebook_id,
            'git': git_meta, 'message': message}
    res = api.post_commit(run_id, data)
    experiment_id = res['experimentId']

    print(f'[swiftace] Commit {experiment_id} successful.')

    if init_new_session:
        new_session(force=True, log=False)

    return linkify("View in Dashboard", res['url'])
