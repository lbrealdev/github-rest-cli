# Justfile for Python

set dotenv-load := true

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
