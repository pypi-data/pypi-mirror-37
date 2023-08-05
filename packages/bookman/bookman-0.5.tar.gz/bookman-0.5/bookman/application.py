# -*- coding: utf-8 -*-
################################################################################
# This file is part of bookman.
#
# Copyright 2018 Richard Paul Baeck <richard.baeck@free-your-pc.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE. 
################################################################################

import os

import gettext
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio,Gtk

from .main_window import MainWindow

class BookmanApplication(Gtk.Application):
    appName = "bookman"
    window = None

    def __init__(self, args):
        gettext.bindtextdomain(self.appName)
        gettext.textdomain(self.appName)
        _ = gettext.gettext

        Gtk.Application.__init__(self, application_id="com.free-your-pc.bookman",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.window = MainWindow(self)

    def do_activate(self):
        self.window.show()
