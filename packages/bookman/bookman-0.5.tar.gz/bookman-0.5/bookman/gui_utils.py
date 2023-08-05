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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class GUIUtils():
    def browse_file(self, parent_window : Gtk.Window) -> str:
        '''
        Displays a dialog to choose a file.
        
        Returns:
        - None if the dialog was canceled
        - A filename as string
        '''
        
        file_name = None
        
        action = Gtk.FileChooserAction.OPEN

        file_dialog = Gtk.FileChooserDialog("Browse files", parent_window,
                                            action,
                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = file_dialog.run() 
        
        if response == Gtk.ResponseType.OK:
            file_name = file_dialog.get_filename()

        file_dialog.destroy() 
        
        return file_name
   
    
GUI_UTILS_SINGLETON = GUIUtils()

