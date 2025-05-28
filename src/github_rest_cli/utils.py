from rich import print as rprint
from dynaconf import settings
from dynaconf.validator import Validator
from dynaconf.base import ValidationError


def rich_output(message: str, format_str: str = "bold green"):
    rprint(f"[{format_str}]{message}[/{format_str}]")


def validate_github_token():
    validator = Validator(
        "AUTH_TOKEN",
        must_exist=True,
        messages={
            "must_exist_true": "Error: Environment variable GITHUB_AUTH_TOKEN is not set. Please set it and try again."
        }
    )

    try:
        validator.validate(settings)
    except ValidationError as e:
        print(e)
        raise SystemExit(1)
