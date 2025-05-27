# Justfile for Python

set dotenv-load := true

test:
  @echo {{justfile_directory()}}

cc:
  uv clean cache