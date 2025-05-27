# Justfile for Python

set dotenv-load := true

# Alias

alias dl := dynaconf-list
alias dv := dynaconf-validate

test:
    @echo {{ justfile_directory() }}

cc:
    uv clean cache

setup-ruff:
    uv tool install ruff

lint:
    ruff check .

fmt:
    ruff format .

dynaconf-list:
    dynaconf -i github_rest_cli.config.settings list

dynaconf-validate:
    dynaconf -i github_rest_cli.config.settings validate
