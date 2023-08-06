# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2019 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

from everett.manager import (
    NO_VALUE,
    ConfigEnvFileEnv,
    ConfigManager,
    ConfigOSEnv,
    ListOf,
    parse_bool,
)

DEBUG = False

# Global experiment placeholder. Should be set by the latest call of Experiment.init()
experiment = None

# Global Optimizer
optimizer = None

DEFAULT_UPLOAD_SIZE_LIMIT = 100 * 1024 * 1024  # 100 MebiBytes


def parse_str_or_identity(_type):
    def parse(value):
        if not isinstance(value, str):
            return value

        return _type(value)

    return parse


PARSER_MAP = {
    str: parse_str_or_identity(str),
    int: parse_str_or_identity(int),
    float: parse_str_or_identity(float),
    bool: parse_str_or_identity(parse_bool),
    list: parse_str_or_identity(ListOf(str)),
}


class Config(object):
    def __init__(self, config_map):
        self.config_map = config_map
        self.override = {}
        self.manager = ConfigManager([ConfigOSEnv(), ConfigEnvFileEnv(".env")])

    def __setitem__(self, name, value):
        self.override[name] = value

    def __getitem__(self, name):
        # Config
        config_type = self.config_map[name].get("type", str)
        parser = PARSER_MAP[config_type]
        config_default = self.config_map[name].get("default", None)

        if name in self.override:
            return self.override[name]

        # Value
        splitted = name.split(".")

        value = self.manager(
            splitted[-1], namespace=splitted[:-1], parser=parser, raise_error=False
        )

        if value == NO_VALUE:
            return parser(config_default)

        return value


CONFIG_MAP = {
    "comet.api_key": {"type": str},
    "comet.offline_directory": {"type": str},
    "comet.url_override": {"type": str, "default": "https://www.comet.ml/clientlib/"},
    "comet.optimization_override": {
        "type": str,
        "default": "https://optimizer.comet.ml/",
    },
    "comet.logging.file": {"type": str},
    "comet.logging.file_level": {"type": str, "default": "INFO"},
    "comet.override_feature.sdk_gpu_monitor": {
        "type": bool
    },  # Leave feature toggle default to None
    "comet.override_feature.sdk_git_patch": {
        "type": bool
    },  # Leave feature toggle default to None,
    "comet.override_feature.sdk_http_logging": {
        "type": bool
    },  # Leave feature toggle default to None
}


def get_config():
    return Config(CONFIG_MAP)
