# Github REST API


### Use

This python cli app uses dynaconf to manage secrets and environment variables.

So that you can use your secrets and environment variables declared in `settings.toml` or `.settings.toml`, use the `GITHUB` prefix value of `envvar_prefix` declared in config.py.

Install pip requirements:
```shell
pip3 install -r requirements.txt
```

Set **github** environment variables:
```shell
export GITHUB_USER="<github-username>"
export GITHUB_AUTH_TOKEN="your-github-auth-token"
```
