import logging.config  # pragma: no cover
import os  # pragma: no cover

import yaml  # type: ignore


def setup_logging(
    path: str = "/opt/working/logging.yaml", default_level: int = logging.INFO
) -> None:  # pragma: no cover
    """Setup logging configuration

    Args:
        path (str, optional): path to where to collect logging config file from. Defaults to 'logging.yaml'.
        default_level (int, optional): Logging level to set at default level if no configuration file found. Defaults to logging.INFO.
    """
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
