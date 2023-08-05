# Sentry Django Settings

This is a package for Django that allows you to add Sentry integration by adding a Django setting.

## Installation

`pip install sentry_django_settings`

Add `sentry_django_settings.apps.Sentry` to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    # ...
    'sentry_django_settings.apps.Sentry',
    # ...
]
```

Add a setting like the following to your `settings.py` file:

```python
SENTRY = {
    'enabled': True,
    'dsn': "https://2e2ac79f64d34e4b85c3a3173e343464@sentry.mysite.com/5",
    'environment': "dev",  # Optional
    'release': '1.0',  # Optional
}
```

`enabled` is a boolean if Sentry should be initialized or not.

To find the DSN in Sentry:

- Go to the project settings in Sentry
- Under `Data`, select `Error Tracking`
- Click "Get your DSN."
- Use the "Public DSN" in all cases.

The `environment` should be appropriate to environment where the server will be running.

The `release` can be any string, but a good option is for it to be either the Git `sha`, or a deployment variable, such as from Bamboo.

The following recommended code requires the GitPython package: `pip install gitpython`. It attempts to get the Git `sha` from the Git repo, if it exists, otherwise it gets it from the Bamboo deployment variable `bamboo_planRepository_revision`.

```python
import os
import git

def get_release():
    # Get Git sha, if it's a Git repo.
    try:
        repo = git.Repo(search_parent_directories=True)
        return repo.head.object.hexsha
    except git.InvalidGitRepositoryError:
        pass
    
    # Get the release from the environment
    return os.environ.get("bamboo_planRepository_revision")
```
