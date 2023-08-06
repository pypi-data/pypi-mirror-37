from .parse import (
    get_version, 
    increment_version, 
    SECTIONS, 
    write_git_version, 
    write_python_version,
    version_to_string,
    commit_git_changes
)    


def bump(args):
    version = get_version()
    section = [s for s in SECTIONS if args[s]][0]
    new_version = increment_version(version, section)
    answer = ask("Version will be bumped from %s to %s. Are you sure?" % (
        version_to_string(version), version_to_string(new_version)))
    if answer:
        write_python_version(new_version)
        write_git_version(new_version)
        commit_git_changes()

    print("Bumped version to %s" % (version_to_string(new_version), ))


def print_version():
    print(version_to_string(get_version))


def ask(question, yes="yes", no="no"):
    while True:
        answer = input("%s [%s]%s/[%s]%s\n> " % (question, yes[0], yes[1:], no[0], no[1:]))
        if yes.startswith(answer.lower()):
            return True
        elif no.startswith(answer.lower()):
            return False

