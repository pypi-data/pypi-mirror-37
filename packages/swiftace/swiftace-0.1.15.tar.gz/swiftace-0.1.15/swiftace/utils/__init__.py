"""Everything other than the top-level API"""
import re
from IPython.core.display import display, HTML
from swiftace.utils import api

NAME_HINT = "Project name can only contain alphabets(a-z), digits(0-9), underscores (_) and hyphens (-)."


class TrackingError(Exception):
    """Error class for exceptions related to experiment tracking"""
    pass


def validate_project_name(name):
    """Validate the project name"""
    if not name:
        raise TrackingError("Project name cannot be empty.")
    if not re.match('^[A-Za-z0-9-_]+$', name):
        raise TrackingError(f"Invalid project name :'{name}'.\n{NAME_HINT}")


def init_experiment(project_slug):
    """Initializes experiment"""
    if not project_slug:
        print(
            "[swiftace] Please initialize project first using: swiftace.init(\"<PROJECT-NAME>\")")
        return
    return api.create_experiment_run(project_slug)


def linkify(text, url=None):
    if url is None:
        url = text
    return display(HTML(f'<a href="{url}" target="_blank">{text}</a>'))
