# Sky Plus Remote
# Copyright (C) 2015 James Scholes
# This program is free software, licensed under the terms of the GNU General Public License (version 3 or later).
# See the file LICENSE.txt for more details.
import os
import os.path
import sys

import application

def get_user_application_data_path():
    return os.path.expandvars('%appdata%')

def setup():
    if application.is_frozen:
        application.application_path = os.path.dirname(sys.executable)
    else:
        application.application_path = os.path.dirname(os.path.abspath(__file__))
    application.config_directory = os.path.join(get_user_application_data_path(), application.internal_name)
    if not os.path.exists(application.config_directory):
        os.mkdir(application.config_directory)
    application.config_file = os.path.join(application.config_directory, '{0}.ini'.format(application.internal_name))
