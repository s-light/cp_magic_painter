# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

"""Config Base Class"""

import json

import board

import helper
import prettyprint
from configdict import extend_deep

# import config as config_file


class ConfigBaseClass(object):
    config_defaults = {}
    config = {}

    def __init__(self, *, config={}):
        super(ConfigBaseClass, self).__init__()
        self.config = config

        self.config_extend_with_defaults(defaults=ConfigBaseClass.config_defaults)

    def load_config_from_file(self, filename="/config.json"):
        config = None
        try:
            with open(filename, mode="r") as configfile:
                config = json.load(configfile)
                configfile.close()
        except OSError as e:
            # print(dir(e))
            # print(e.errno)
            if e.errno == 2:
                print(e)
                # print(e.strerror)
            else:
                raise e
        return config

    def config_extend_with_defaults(self, *, defaults):
        # extend with default config - thisway it is safe to use ;-)
        # extend_deep(self.config, self.config_defaults.copy())
        extend_deep(self.config, defaults.copy())

    def config_print(self, *, config=None, line_pre=""):
        if config is None:
            config = self.config
        prettyprint.pretty_print(container=config, line_pre=line_pre)
    
    