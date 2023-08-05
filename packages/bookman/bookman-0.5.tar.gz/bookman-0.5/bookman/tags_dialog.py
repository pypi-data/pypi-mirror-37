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
from _sqlite3 import Row
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import CONFIG_SINGLETON
from .models import Tag

class TagsDialog:
    def __init__(self, app, bookmarks):
        # Dialog
        self.dialog = None
        
        # Tree
        self.tree_model = None
        
        # Reference to bookmarks
        self.bookmarks = bookmarks


        builder = Gtk.Builder()
        builder.set_translation_domain(app.appName)
        builder.add_from_file(CONFIG_SINGLETON.get_absolute_path(CONFIG_SINGLETON.get_config()["Builder"]["Files"]["TagsDialog"]))
        builder.connect_signals(self)
        
        self.init_dialog(builder)
        self.init_tree(builder)
        
        self.bookmarks_to_tree(bookmarks, self.tree_model)


    def init_dialog(self, builder : Gtk.Builder):
        self.dialog = builder.get_object('tags_dialog')

        refresh_button = builder.get_object('refresh_button')
        refresh_button.connect("clicked", self.on_refresh_clicked)

        cancel_button = builder.get_object('close_button')
        cancel_button.connect("clicked", self.on_close_clicked)


    def init_tree(self, builder : Gtk.Builder):
        self.tree_model = builder.get_object("main_tree_store")
        tree_view = builder.get_object("main_tree")
        
        
    def tag_to_tree_row(self, tag : Tag) -> ( ):
        row = ( tag.name, )
        
        return row
    
        
    def bookmarks_to_tree(self, bookmarks, tree_model : Gtk.TreeModel) -> [ ]:
        tags = [ ]
        
        for bookmark in bookmarks:
            for tag in bookmark.tags:
                tag_already_stored = False

                for stored_tag in tags:
                    if tag.name == stored_tag.name:
                        tag_already_stored = True
                        break
                
                if tag_already_stored == False:
                    tags.append(tag)
                    row = self.tag_to_tree_row(tag)
                    tree_model.append(row) 
                    
                    
    def refresh(self):
        self.tree_model.clear()
        self.bookmarks_to_tree(self.bookmarks, self.tree_model)
            
                    
    def on_refresh_clicked(self, button : Gtk.Button):
        self.refresh()
        

    def on_close_clicked(self, button : Gtk.Button):
        self.dialog.destroy()


    def run(self):
#         response = self.dialog.run()
#         self.dialog.destroy()
        self.dialog.present()
