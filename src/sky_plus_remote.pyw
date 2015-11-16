# Sky Plus Remote
# Copyright (C) 2015 James Scholes
# This program is free software, licensed under the terms of the GNU General Public License (version 3 or later).
# See the file LICENSE.txt for more details.
import sys

import wx

import application

def main():
    application.wx_app = wx.App(False)

    single_instance_checker = wx.SingleInstanceChecker()
    if single_instance_checker.IsAnotherRunning():
        wx.MessageBox('Another instance of Sky Plus Remote is already running.', 'Error', wx.ICON_ERROR)
        sys.exit(1)

    import paths
    paths.setup()
    import log
    log.setup()
    logger = application.logger
    logger.info('Starting application: {0}'.format(application.title))
    logger.info('Application version: {0}'.format(application.version))
    logger.info('Application directory: {0}'.format(application.application_path))
    logger.info('Application config directory: {0}'.format(application.config_directory))

    import config
    try:
        config.setup()
    except config.ConfigLoadError:
        wx.MessageBox('Unfortunately, there was a problem loading your configuration settings.  The application will now exit.', 'Configuration Error', wx.ICON_ERROR)
        sys.exit(1)

    import gui
    gui.setup()
    application.wx_app.MainLoop()

if __name__ == '__main__':
    main()