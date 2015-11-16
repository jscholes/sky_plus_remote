# Sky Plus Remote
# Copyright (C) 2015 James Scholes
# This program is free software, licensed under the terms of the GNU General Public License (version 3 or later).
# See the file LICENSE.txt for more details.
import collections

import wx
import wx.lib.sized_controls as sc

import application

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

    def onFilesListKeyPressed(self, event):
        if event.GetKeyCode() == wx.WXK_DELETE and self.files_list.GetCount() != 0:
            self.remove_file(self.files_list.GetSelection())
        else:
            event.Skip()

def setup():
    application.main_window = MainWindow()
    application.wx_app.SetTopWindow(application.main_window)
    application.main_window.Show()
