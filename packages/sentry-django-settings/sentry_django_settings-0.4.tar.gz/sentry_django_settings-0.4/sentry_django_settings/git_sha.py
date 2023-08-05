from __future__ import absolute_import, unicode_literals

import git


def get_from_repo():
    """Get Git SHA, if it's a Git repo."""
    try:
        repo = git.Repo(search_parent_directories=True)
        return repo.head.object.hexsha
    except git.InvalidGitRepositoryError:
        pass


def get_from_file(path):
    """Get the SHA from the deployment git_sha file."""
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except IOError:
        pass