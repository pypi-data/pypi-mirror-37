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
    'git_sha_path': './git_sha'  # Optional
}
```

`enabled` is a boolean if Sentry should be initialized or not.

To find the DSN in Sentry:

- Go to the project settings in Sentry
- Under `Data`, select `Error Tracking`
- Click "Get your DSN."
- Use the "Public DSN" in all cases.

The `environment` should be appropriate to environment where the server will be running.

The `release` can be any string. If left blank or excluded and this is being run inside of a Git repo, the Git SHA will be used instead. Note: If `release` is defined, then `git_sha_path` is ignored.

The `git_sha_path` is a path to a file that contains the Git SHA string. This is useful when deploying via a packaging service. During packaging, create a file that has the Git SHA, then reference it in this setting. Note: If `release` is defined, then `git_sha_path` is ignored.
