# Sky Plus Remote
# Copyright (C) 2015 James Scholes
# This program is free software, licensed under the terms of the GNU General Public License (version 3 or later).
# See the file LICENSE.txt for more details.
from io import StringIO
import os.path
import sys

from configobj import ConfigObj, ConfigObjError
from validate import Validator

import application

class ConfigLoadError(Exception):
    pass

def setup():
    config_spec = StringIO('''ip_address = string()
    skyplay_endpoint = string()
    request_timeout = integer(default=3)''')

    try:
        config = ConfigObj(infile=application.config_file, configspec=config_spec, create_empty=True, encoding='UTF8', unrepr=True)
    except ConfigObjError:
        application.logger.critical('Error loading config from: {0}'.format(application.config_file), exc_info=sys.exc_info())
        raise ConfigLoadError
        return
    application.config_validator = Validator()
    config.validate(application.config_validator, copy=True)
    config.write()
    application.config = config
    application.logger.info('Loaded configuration file: {0}'.format(application.config_file))
