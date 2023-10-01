# Github REST API


### Use

This python cli app uses dynaconf to manage secrets and environment variables.

So that you can use your secrets and environment variables declared in `settings.toml` or `.settings.toml`, use the `GITHUB` prefix value of `envvar_prefix` declared in config.py.

Set up python packages dependencies from `pyproject.toml`:
```shell
run rync
```

Export required environment variables:
```shell
export GITHUB_USER="<github-username>"
export GITHUB_AUTH_TOKEN="<github-auth-token>"
```

Run the Github REST API cli:
```shell
python github-rest-api -h
```

### Set up dynaconf

After install dynaconf via pip, run this commando to init a dynaconf project at the root of project:
```shell
dynaconf init
```

This will create the following files:
```shell
├── ./config.py
├── ./.gitignore
├── ./__pycache__
├── ./.secrets.toml
├── ./settings.toml
└── ./venv
```

List all defined parameters: 
```shell
dynaconf -i config.settings list
```

To use github-rest-api.py cli, export the following environment variables:
```shell
export GITHUB_USER="<github-username>"
export GITHUB_AUTH_TOKEN="<github-auth-token>"
```

