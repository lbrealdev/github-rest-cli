from dynaconf import Dynaconf, Validator

DEFAULT_API_URL = "https://api.github.com"

settings = Dynaconf(
    envvar_prefix="GITHUB",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    env_switcher="SET_ENV",
    validators=[
        Validator("API_URL", default=DEFAULT_API_URL),
    ],
)

# The CLI will not work if AUTH_TOKEN is not set (GITHUB_AUTH_TOKEN).
AUTH_TOKEN_VALIDATOR = Validator(
    "AUTH_TOKEN",
    must_exist=True,
    messages={
        "must_exist_true": "Environment variable GITHUB_AUTH_TOKEN is not set. Please set it and try again."
    },
)
