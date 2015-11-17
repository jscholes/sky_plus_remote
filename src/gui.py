# Sky Plus Remote
# Copyright (C) 2015 James Scholes
# This program is free software, licensed under the terms of the GNU General Public License (version 3 or later).
# See the file LICENSE.txt for more details.
import collections
import sys
import threading

import wx
import wx.lib.sized_controls as sc

import application
import controller
from signals import successful_connection, connection_error

def create_button(parent, label='', callback=None, id=-1):
    control = wx.Button(parent, id=id, label=label)
    if callback and isinstance(callback, collections.Callable):
        control.Bind(wx.EVT_BUTTON, callback)

    return control

def create_labelled_field(parent, label=None, text='', read_only=False):
    control_label = wx.StaticText(parent, label=label)
    control = wx.TextCtrl(parent, -1, text)
    control.SetSizerProps(expand=True)

    if read_only:
        control.SetWindowStyle(wx.TE_READONLY|wx.TE_NO_VSCROLL|wx.TE_MULTILINE)

    return control



class BaseDialog(sc.SizedDialog):
    def __init__(self, parent, *args, **kwargs):
        super(BaseDialog, self).__init__(parent=parent, id=-1, title=self._title, style=wx.DEFAULT_DIALOG_STYLE, *args, **kwargs)
        self.Centre(wx.BOTH)
        self.panel = self.GetContentsPane()
        self.panel.SetSizerType('form')
        self.setup_layout()
        self.Fit()

    def setup_layout(self):
        raise NotImplementedError



class ConnectionDialog(BaseDialog):
    def __init__(self, parent, *args, **kwargs):
        self._title = 'Sky Plus Remote'
        self.initial_progress = 'To get started, please enter the IP address of your Sky Plus HD box.'
        successful_connection.connect(self.onSuccessfulConnection)
        connection_error.connect(self.onConnectionError)
        super(ConnectionDialog, self).__init__(parent=parent, *args, **kwargs)

    def setup_layout(self):
        self.progress_text = wx.StaticText(self.panel, label=self.initial_progress)
        self.ip_address = create_labelled_field(self.panel, label='&IP Address')

        button_sizer = wx.StdDialogButtonSizer()
        self.connect_button = create_button(self.panel, '&Connect', self.onConnect)
        button_sizer.AddButton(self.connect_button)
        self.cancel_button = wx.Button(self.panel, wx.ID_CANCEL)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)
        button_sizer.AddButton(self.cancel_button)
        self.SetButtonSizer(button_sizer)
        self.SetEscapeId(wx.ID_CANCEL)

    def onSuccessfulConnection(self, sender, **kwargs):
        wx.CallAfter(self.EndModal, wx.ID_OK)

    def onError(self, error_message):
        wx.MessageBox(error_message, 'Error', wx.ICON_ERROR, parent=self)
        self.progress_text.SetLabel(self.initial_progress)
        self.ip_address.Clear()
        self.ip_address.Show()
        self.connect_button.Show()
        self.ip_address.SetFocus()

    def onConnectionError(self, sender, **kwargs):
        wx.CallAfter(self.onError, kwargs['error_msg'])

    def onConnect(self, event):
        if not self.ip_address.GetValue():
            wx.MessageBox('Please enter an IP address.', 'Error', wx.ICON_ERROR, parent=self)
            self.ip_address.SetFocus()
            return

        self.cancel_button.SetFocus()
        self.ip_address.Hide()
        self.connect_button.Hide()
        self.progress_text.SetLabel('Connecting...')
        controller.connect_to_box(self.ip_address.GetValue())

    def onCancel(self, event):
        self.EndModal(wx.ID_CANCEL)



class MainWindow(sc.SizedFrame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(None, -1, application.title, size=(800, 600), style=wx.DEFAULT_FRAME_STYLE, *args, **kwargs)
        self.Centre()
        self.setup_layout()

    def setup_layout(self):
        main_panel = self.GetContentsPane()
        main_panel.SetSizerType('vertical')

        channels_list_label = wx.StaticText(main_panel, label='&Channels')
        self.channels_list = wx.ListBox(main_panel, style=wx.LB_NEEDED_SB)
        self.channels_list.SetSizerProps(expand=True, proportion=1)
        # self.channels_list.Bind(wx.EVT_KEY_DOWN, self.onFilesListKeyPressed)

        self.status_bar = wx.StatusBar(self)
        self.status_bar.SetStatusText('Connected to: {0}'.format(application.box.ip_address))
        self.SetStatusBar(self.status_bar)

    def onFilesListKeyPressed(self, event):
        if event.GetKeyCode() == wx.WXK_DELETE and self.files_list.GetCount() != 0:
            self.remove_file(self.files_list.GetSelection())
        else:
            event.Skip()

def setup():
    box_ip = application.config.get('ip_address', '')
    if not box_ip:
        connection_dialog = ConnectionDialog(None)
        result = connection_dialog.ShowModal()
        if result == wx.ID_CANCEL:
            sys.exit()

    device_info = 'Connected to: {0}\nModel: {1}\nFriendly name: {2}\nManufacturer: {3}\nChip ID: {4}\nUDN: {5}'.format(
        application.box.ip_address,
        application.box.model,
        application.box.friendly_name,
        application.box.manufacturer,
        application.box.chip_id,
        application.box.udn
    )

    wx.MessageBox(device_info, 'Information', wx.ICON_INFORMATION)

    application.main_window = MainWindow()
    application.wx_app.SetTopWindow(application.main_window)
    application.main_window.Show()
