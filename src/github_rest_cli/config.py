from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="GITHUB",
    settings_files=["../../settings.toml", "../../.secrets.toml"],
    environments=["development", "testing", "production"],
    env_switcher="SET_ENV",
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
