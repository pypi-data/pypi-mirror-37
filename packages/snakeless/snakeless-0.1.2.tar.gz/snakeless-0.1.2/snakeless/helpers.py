from contextlib import contextmanager

from halo import Halo
from yaml import load

from .constants import CONFIG_VALIDATOR, PROVIDERS
from .exceptions import CommandFailure

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


@contextmanager
def snakeless_spinner(*args, **kwargs):
    spinner = Halo(*args, **kwargs)
    spinner.start()
    try:
        yield spinner
    except CommandFailure as exc:
        spinner.fail(str(exc))
        raise
    except Exception as exc:
        spinner.fail(
            spinner.text
            + "\n"
            + "Unexpected exception."
        )
        raise
    finally:
        spinner.stop()


def check_config_existence(root_fs, file_name="snakeless.yml"):
    return root_fs.exists(file_name)


def get_provider(provider_name, config):
    return PROVIDERS[provider_name](config)


def parse_config(
    root_fs, file_name="snakeless.yml", validator=CONFIG_VALIDATOR
):
    config_file_data = root_fs.gettext("snakeless.yml")
    raw_parsed_config = load(config_file_data, Loader=Loader)
    parse_config = validator.validate(raw_parsed_config)
    # validate a few more fields mannualy
    return parse_config
