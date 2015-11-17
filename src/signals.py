# Sky Plus Remote
# Copyright (C) 2015 James Scholes
# This program is free software, licensed under the terms of the GNU General Public License (version 3 or later).
# See the file LICENSE.txt for more details.
from blinker import signal

successful_connection = signal('successful_connection')
connection_error = signal('connection_error')
