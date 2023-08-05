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

import copy

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import CONFIG_SINGLETON
from .gui_utils import GUI_UTILS_SINGLETON

class PereferencesDialog:
    """Changes a copy of the global configuration but does not change the gloal
    configuration itself.
    """

    def __init__(self, app):
        # Dialog
        self.dialog = None
       
        # Fields 
        self.doubleclick_execute_entry = None
        self.autobackup_checkbox = None
        self.autobackup_suffix_entry = None
        
        builder = Gtk.Builder()
        builder.set_translation_domain(app.appName)
        builder.add_from_file(CONFIG_SINGLETON.get_absolute_path(CONFIG_SINGLETON.get_config()["Builder"]["Files"]["PreferencesDialog"]))
        builder.connect_signals(self)
        
        self.init_dialog(builder)
        self.init_fields(builder)
        
    
    def init_dialog(self, builder : Gtk.Builder):
        self.dialog = builder.get_object('preferences_dialog')
        
        cancel_button = builder.get_object('cancel_button')
        cancel_button.connect("clicked", self.on_cancel_clicked)

        save_button = builder.get_object('save_button')
        save_button.connect("clicked", self.on_save_clicked)
        
        
    def init_fields(self, builder : Gtk.Builder):
        self.doubleclick_execute_entry = builder.get_object('doubleclick_execute_entry')
       
        self.autobackup_checkbox = builder.get_object('autobackup_checkbox')
       
        self.autobackup_suffix_entry = builder.get_object('autobackup_suffix_entry')
        
        self.default_file_entry = builder.get_object('default_file_entry')
        self.default_file_button = builder.get_object('default_file_button')
        self.default_file_button.connect("clicked", self.on_default_file_clicked)

        
    def on_cancel_clicked(self, button : Gtk.Button):
        self.dialog.response(Gtk.ResponseType.CANCEL)
   
   
    def on_save_clicked(self, button : Gtk.Button):
        self.dialog.response(Gtk.ResponseType.OK)
        
    
    def on_default_file_clicked(self, button : Gtk.Button):
        filename = GUI_UTILS_SINGLETON.browse_file(None)
        
        if filename is not None:
            self.default_file_entry.set_text(filename)
            
        
    def config_to_gui(self, config, doubleclick_execute_entry : Gtk.Entry,
                      autobackup_checkbox : Gtk.CheckButton, autobackup_suffix_entry : Gtk.Entry,
                      default_file_entry : Gtk.Entry):
        doubleclick_execute_entry.set_text(config["Preferences"]["Doubleclick_Execute"])
        autobackup_checkbox.set_active(config["Preferences"]["Autobackup"])
        autobackup_suffix_entry.set_text(config["Preferences"]["Autobackup_Suffix"])
        default_file_entry.set_text(config["Preferences"]["Default_Database_File"])
        

    def gui_to_config(self, config, doubleclick_execute_entry : Gtk.Entry,
                      autobackup_checkbox : Gtk.CheckButton, autobackup_suffix_entry : Gtk.Entry,
                      default_file_entry : Gtk.Entry):
        config["Preferences"]["Doubleclick_Execute"] = doubleclick_execute_entry.get_text()
        config["Preferences"]["Autobackup"] = autobackup_checkbox.get_active()
        config["Preferences"]["Autobackup_Suffix"] = autobackup_suffix_entry.get_text()
        config["Preferences"]["Default_Database_File"] = default_file_entry.get_text()

        
    def run(self):
        """
        If "Save" was clicked, then the changed copy of the global config is returned,
        otherwise None.
        """
        config = copy.deepcopy(CONFIG_SINGLETON.get_config())
       
        self.config_to_gui(config, self.doubleclick_execute_entry, self.autobackup_checkbox,
                           self.autobackup_suffix_entry, self.default_file_entry)
        
        response = self.dialog.run()
        
        if response != Gtk.ResponseType.OK:
            config = None
        else:
            self.gui_to_config(config, self.doubleclick_execute_entry, self.autobackup_checkbox,
                               self.autobackup_suffix_entry, self.default_file_entry)
            
        self.dialog.destroy()
   
        return config
    
