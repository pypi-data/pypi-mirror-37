import os
import importlib
import re
import subprocess


VERSION_REGEX = re.compile(
    r'(?:__)?version(?:__)?\s*=\s*"(\d+)\.(\d+)\.(\d+)(-\w+)?"', 
    re.MULTILINE
)
SECTIONS = ('major', 'minor', 'patch')


def get_version() -> tuple:
    init_path = get_init_path()
    with open(init_path, 'r') as source:
        match = VERSION_REGEX.search(source.read())
        return tuple(map(int, filter(bool, match.groups())))


def increment_version(version: tuple, section: str) -> tuple:
    try:
        return update_tuple(version, SECTIONS.index(section), lambda x: x+1)
    except Exception:
        if section == 'label':
            raise NotImplementedError
        else:
            raise ValueError("Unknown version section: {}".format(section))


def write_python_version(version) -> None:
    if isinstance(version, tuple):
        version = version_to_string(version)

    init_path = get_init_path()
    with open(init_path, 'r') as target:
        content = target.read()
    with open(init_path, 'w') as target:
        target.write(VERSION_REGEX.sub('__version__ = "{}"'.format(version), content))

    try:
        with open("setup.py", 'r') as target:
            content = target.read()
        with open("setup.py", 'w') as target:
            target.write(VERSION_REGEX.sub('version="{}"'.format(version), content))
    except:
        pass

    print("Wrote version")


def write_git_version(version) -> None:
    if isinstance(version, tuple):
        version = version_to_string(version)

    subprocess.call(["git", "tag", version])


def commit_git_changes() -> None:
    init_path = get_init_path()
    subprocess.call(["git", "add", init_path])
    subprocess.call(["git", "commit", "-m", "'Bumped version'"])


def get_project_name() -> str:
    return os.path.split(os.getcwd())[1]


def get_init_path() -> str:
    return os.path.join(os.path.split(os.getcwd())[1], "__init__.py")


def is_git() -> bool:
    return os.path.exists(".git")


def update_tuple(t, index, function):
    return t[:index] + (function(t[index]), ) + t[index+1:]


def version_to_string(version):
    return '.'.join(str(x) for x in version)
