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
import time

import gi
from sqlalchemy.sql.expression import except_
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import CONFIG_SINGLETON
from .utils import FirefoxBookmarkTransformator
from .preferences_dialog import PereferencesDialog
from .tags_dialog import TagsDialog
from .models import DATABASE_SINGLETON
from .models import Bookmark
from .models import Tag

class MainWindow():
    TAGS_SEPARATOR = ', '
    
    def __init__(self, app):
        # Application
        self.app = None
        self.path = None
        self.clipboard = None
        
        # Window
        self.window = None
    
        # Tree input
        self.current_new_number = 0
        self.tree_selection = None
        self.tree_model = None
        self.filter_by_filter = None
        self.filter_by_entry = None
        self.current_bookmarks = []
            
        # Input entries
        self.name_entry = None
        self.url_entry = None
        self.tags_entry = None
        self.open_with_entry = None
        self.description_textview = None
        self.detail_ok_button = None
       
        
        self.xml_filename = CONFIG_SINGLETON.get_absolute_path(CONFIG_SINGLETON.get_config()["Builder"]["Files"]["MainWindow"])
        self.app = app
        self.current_new_number = 1
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        
        builder = Gtk.Builder()
        builder.set_translation_domain(self.app.appName)
        builder.add_from_file(self.xml_filename)
        builder.connect_signals(self)

        self.init_window(builder)
        self.init_menus(builder)
        self.init_toolbar(builder)
        self.init_tree(builder)
        
        self.load_default_file()
        

    def init_window(self, builder : Gtk.Builder):
        self.window = builder.get_object("main_window")
        self.window.connect("destroy", self.on_quit)
        
        self.filter_by_entry = builder.get_object('filter_by_entry')
        self.filter_by_entry.connect('activate', self.on_filter_by_changed)
        
        self.name_entry = builder.get_object("name_entry")
        self.url_entry = builder.get_object("url_entry")
        self.tags_entry = builder.get_object("tags_entry")
        self.open_with_entry = builder.get_object("open_with_entry")
        self.description_textview = builder.get_object("description_textview")
        
        self.detail_ok_button = builder.get_object("ok_button")
        self.detail_ok_button.connect("clicked", self.on_ok_clicked)
        

    def init_menus(self, builder : Gtk.Builder):
        accel_group_ctrl = Gtk.AccelGroup();
        accel_group_alt = Gtk.AccelGroup();
        self.window.add_accel_group(accel_group_ctrl);
        self.window.add_accel_group(accel_group_alt);

        # File
        menuitem = builder.get_object("menuitem_quit")
        menuitem.connect("activate", self.on_quit)
        menuitem.add_accelerator("activate", accel_group_ctrl, ord('q'),
                                 Gdk.ModifierType.CONTROL_MASK,
                                 Gtk.AccelFlags.VISIBLE)

        menuitem = builder.get_object("menuitem_save")
        menuitem.connect("activate", self.on_save)
        menuitem.add_accelerator("activate", accel_group_ctrl, ord('s'),
                                 Gdk.ModifierType.CONTROL_MASK,
                                 Gtk.AccelFlags.VISIBLE)

        menuitem = builder.get_object("menuitem_save_as")
        menuitem.connect("activate", self.on_save_as)

        menuitem = builder.get_object("menuitem_new")
        menuitem.connect("activate", self.on_new)
        menuitem.add_accelerator("activate", accel_group_ctrl, ord('n'),
                                 Gdk.ModifierType.CONTROL_MASK,
                                 Gtk.AccelFlags.VISIBLE)

        menuitem = builder.get_object("menuitem_open")
        menuitem.connect("activate", self.on_open)
        menuitem.add_accelerator("activate", accel_group_ctrl, ord('o'),
                                 Gdk.ModifierType.CONTROL_MASK,
                                 Gtk.AccelFlags.VISIBLE)
       
        # Edit 
        menuitem = builder.get_object("menuitem_paste_url")
        menuitem.connect("activate", self.on_paste_url)
        key, mod = Gtk.accelerator_parse("<Alt>v")
        menuitem.add_accelerator("activate", accel_group_alt, 
                                 key, mod,
                                 Gtk.AccelFlags.VISIBLE)

        menuitem = builder.get_object("menuitem_showtags")
        menuitem.connect("activate", self.on_show_tags)

        menuitem = builder.get_object("menuitem_preferences")
        menuitem.connect("activate", self.on_preferences)
 
        # Tools
        menuitem = builder.get_object("menuitem_import_firefox_html")
        menuitem.connect("activate", self.on_import_firefox_html)

        # Help
        menuitem = builder.get_object("menuitem_about")
        menuitem.connect("activate", self.on_about)
        
    
    def init_toolbar(self, builder : Gtk.Builder):
        toolitem = builder.get_object("toolitem_add")
        toolitem.connect("clicked", self.on_add_clicked)

        toolitem = builder.get_object("toolitem_delete")
        toolitem.connect("clicked", self.on_delete_clicked)


    def init_tree(self, builder : Gtk.Builder):
        self.tree_model = builder.get_object("main_tree_store")
        self.filter_by_filter = self.tree_model.filter_new()
        self.filter_by_filter.set_visible_func(self.filter_by_function)
        
        tree_view = builder.get_object("main_tree")
        tree_view.set_model(self.filter_by_filter)
        tree_view.connect("row-activated", self.on_row_doubleclicked)
        
        self.tree_selection = tree_view.get_selection()
        self.tree_selection.connect("changed", self.on_selection_changed)
        
        
        # Set the 1. column editable        
        renderer = builder.get_object("cellrendertext1")
        renderer.connect("edited", self.on_edited_column1)
        renderer.set_property('editable', True)
        
        # Set the 2. column editable        
        renderer = builder.get_object("cellrendertext2")
        renderer.connect("edited", self.on_edited_column2)
        renderer.set_property('editable', True)
        
        
    def load_default_file(self):
        try:
            default_file = CONFIG_SINGLETON.get_config()["Preferences"]["Default_Database_File"]
            if default_file is not None and len(default_file) > 0:
                self.set_path(default_file)
                self.read_and_use_database()
                
        except:
            self.clear_application()
        
    
    def on_edited_column1(self, renderer : Gtk.CellRendererText, 
                          row_id : int, edited : str):
        row = self.tree_model[row_id]
        
        bookmark = self.tree_row_to_bookmark(row)
        old_bookmark = self.get_cache(bookmark.name) 
        if old_bookmark is not None:
            bookmark = old_bookmark
        
        row[0] = edited
        bookmark.name = edited
       
        self.filter_by_filter.refilter()
       
    
    def on_edited_column2(self, renderer : Gtk.CellRendererText, 
                          row_id : int, edited : str):
        row = self.tree_model[row_id]
        bookmark = self.tree_row_to_bookmark(row)
        bookmark = self.get_cache(bookmark.name)
        
        row[1] = edited
        bookmark.url = edited

        self.update_cache(bookmark)

        self.filter_by_filter.refilter()


    def show(self):
        """
        Show the window.
        """
        self.app.add_window(self.window)
        self.window.show()
        
    
    def has_changed(self):
        has_changed = False

        bookmarks = self.current_bookmarks
        
        if self.get_path() == None and len(bookmarks) > 0:
            has_changed = True
        else:
            if self.get_path() != None:
                if DATABASE_SINGLETON.open_database(self.get_path()) == 0:
                    session = DATABASE_SINGLETON.get_session()
                   
                    db_bookmarks = session.query(Bookmark).all() 
                    if len(bookmarks) > len(db_bookmarks) or len(bookmarks) < len(db_bookmarks):
                        has_changed = True
                    else:
                        for db_bookmark in db_bookmarks:
                            found = False
                            
                            for bookmark in bookmarks:
                                if db_bookmark.name == bookmark.name:
                                    found = True
                                    break
                            
                            if found == False:
                                has_changed = True
                                break
                            
                        if has_changed == False:
                            for bookmark in bookmarks:
                                db_bookmarks = session.query(Bookmark).filter(
                                    Bookmark.name == bookmark.name).all()
                                
                                if len(db_bookmarks) == 0:
                                    has_changed = True
     
                                db_bookmark = db_bookmarks[0]
                                if db_bookmark == None: 
                                    has_changed = True
                                elif db_bookmark.name != bookmark.name:
                                    has_changed = True
                                elif db_bookmark.url != bookmark.url: 
                                    has_changed = True
                                elif len(db_bookmark.tags) != len(bookmark.tags):
                                    has_changed = True
                                elif len(db_bookmark.tags) == len(bookmark.tags):
                                    for db_tag in db_bookmark.tags:
                                        has_changed = True
                                        for tag in bookmark.tags:
                                            if db_tag.name == tag.name:
                                                has_changed = False 
                                                break
                                    
                                if has_changed == True:
                                    break 
    
                    DATABASE_SINGLETON.close_database()
        
        return has_changed
    
    
    def get_current_new_number(self):
        """
        Gets the attribute current_new_number and increments it afterwards.
        """
        ret = self.current_new_number
        self.current_new_number = self.current_new_number + 1
        return ret
        

    def get_path(self):
        return self.path


    def set_path(self, path):
        self.path = path


    def set_path_with_dialog(self, set_new_file = False):
        """
        Returns True if the user supplied a valid path. False otherwise.
        """

        changed_path = False
      
        title = "Open file"
        action = Gtk.FileChooserAction.OPEN
        ok_button = Gtk.STOCK_OPEN
        
        if set_new_file == True:
            title = 'Save file'
            action = Gtk.FileChooserAction.SAVE
            ok_button = Gtk.STOCK_SAVE

        file_dialog = Gtk.FileChooserDialog(title, self.window,
                                            action,
                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                             ok_button, Gtk.ResponseType.OK))
        response = file_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.set_path(file_dialog.get_filename())
            changed_path = True

        file_dialog.destroy()

        return changed_path


    def clear_application(self):
        """
        Clears the entire applications in-cache memory of Bookmarks
        """
        self.tree_selection.unselect_all()
        self.filter_by_filter.refilter()
        self.tree_model.clear()
        self.filter_by_filter.refilter()
        self.current_bookmarks = []
      
    
    def get_title_changed(self): 
        title = self.get_title()
        title = '*' + title
        return title
    
    
    def get_title(self):
        title = self.get_path()
        if title == None:
            title = 'New'
            
        title = os.path.basename(title)
            
        return title
    

    def on_quit(self, menuitem : Gtk.MenuItem):
        self.check_changes_and_save()
        self.app.quit()

    def on_save(self, menuitem : Gtk.MenuItem):
        if self.has_changed() == True:
            if self.get_path() == None:
                self.on_save_as(menuitem)
            else:
                if self.write_database() == 0:
                    self.clear_application()
                    if self.read_and_use_database() != 0:
                        self.clear_application()
                        self.read_database_failed_dialog(self.get_path())
                else:
                    self.write_database_failed_dialog(self.get_path())
                
                self.refresh_title()


    def on_save_as(self, menuitem : Gtk.MenuItem):
        has_valid_path = self.set_path_with_dialog(set_new_file = True)
        perform_write = False

        if has_valid_path == True:
            perform_write = True
            
            if os.path.isfile(self.get_path()):
                dialog = Gtk.MessageDialog(text = 'Overwrite file?',
                                           type = Gtk.MessageType.WARNING,
                                           buttons = (Gtk.STOCK_YES, Gtk.ResponseType.YES,
                                                      Gtk.STOCK_NO, Gtk.ResponseType.NO))
                dialog.set_default_response(Gtk.ResponseType.NO)
                response = dialog.run()
                dialog.destroy()
                if response == Gtk.ResponseType.NO:
                    perform_write = False
           
        else:
            # No valid path was selected
            pass
        
        if perform_write == True:
            if self.write_database() == 0: 
                self.clear_application()
                if self.read_and_use_database() != 0:
                    self.clear_application()
                    self.read_database_failed_dialog(self.get_path())
            else:
                self.write_database_failed_dialog(self.get_path())
            
            self.refresh_title()
 

    def on_new(self, menuitem : Gtk.MenuItem):
        self.check_changes_and_save()
        self.clear_application()
        self.set_path(None)


    def on_open(self, menuitem : Gtk.MenuItem):
        self.check_changes_and_save()
        
        changed_path = self.set_path_with_dialog()
        if changed_path == True:
            self.clear_application()
            if self.read_and_use_database() != 0:
                self.clear_application()
                self.read_database_failed_dialog(self.get_path())
                
            self.refresh_title()
            
            
    def on_paste_url(self, menuitem : Gtk.MenuItem):
        url = self.clipboard.wait_for_text()
        
        name = 'Pasted Bookmark ' + str(self.get_current_new_number())
        
        row = (name, url)
        self.tree_model.append(None, row)
        bookmark = self.tree_row_to_bookmark(row)
        self.update_cache(bookmark)
        
        self.filter_by_filter.refilter()
        
        
    def on_show_tags(self, menuitem : Gtk.MenuItem):
        dialog = TagsDialog(self.app, self.current_bookmarks)
        dialog.run()
        
    
    def on_preferences(self, menuitem : Gtk.MenuItem):
        dialog = PereferencesDialog(self.app)
        config = dialog.run()
        
        if config != None:
            CONFIG_SINGLETON.set_config(config)
            CONFIG_SINGLETON.write_config_local()
            CONFIG_SINGLETON.reload_config()
        
        
    def on_import_firefox_html(self, menuitem : Gtk.MenuItem):
        title = "Import bookmarks"
        action = Gtk.FileChooserAction.OPEN
        ok_button = Gtk.STOCK_OPEN
        
        file_dialog = Gtk.FileChooserDialog(title, self.window,
                                            action,
                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                             ok_button, Gtk.ResponseType.OK))
        response = file_dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = file_dialog.get_filename()
            transformator = FirefoxBookmarkTransformator(filename)
            bookmarks = transformator.get_bookmarks()
            for bookmark in bookmarks:
                added = self.update_cache(bookmark)
                if added == 1:
                    row = (bookmark.name, bookmark.url)
                    self.tree_model.append(None, row)
            
            self.filter_by_filter.refilter()
            
        file_dialog.destroy()
    

    def on_about(self, menuitem : Gtk.MenuItem):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_program_name("bookman")
        about_dialog.set_copyright("Richard Paul Bäck, 2018")
        about_dialog.set_website("http://www.free-your-pc.com")
        about_dialog.set_website_label("Free-your-PC")
        about_dialog.set_license("GPLv3")
        about_dialog.connect("response", self.on_about_dialog_close)

        self.app.add_window(about_dialog)
        self.about_dialog = about_dialog
        about_dialog.run()
        

    def on_about_dialog_close(self, action, param):
        """
        Is called when the user clicks the "About" button in the menu
        """

        if self.about_dialog != None:
            self.about_dialog.destroy()
            
    
    def on_add_clicked(self, toolitem : Gtk.ToolButton):
        """
        Is called when the user clicks the "Add" button in the toolbar
        """
        
        name = 'New Bookmark ' + str(self.get_current_new_number())
        url = ''
        row = (name, url)
        self.tree_model.append(None, row)
        bookmark = self.tree_row_to_bookmark(row)
        self.update_cache(bookmark)
        
        self.filter_by_filter.refilter()
        
    
    def on_delete_clicked(self, toolitem : Gtk.ToolButton):
        """
        Is called when the user clicks the "Delete" button in the toolbar
        """
        model, treeiter = self.tree_selection.get_selected()
        if treeiter is not None:
            bookmark = self.tree_row_to_bookmark(model[treeiter])
            
            main_treeiter = self.tree_model.get_iter_first()
            while main_treeiter is not None:
                compare_bookmark = self.tree_row_to_bookmark(self.tree_model[main_treeiter]) 
                if compare_bookmark.name == bookmark.name:
                    del self.tree_model[main_treeiter]
                    break
                
                main_treeiter = self.tree_model.iter_next(main_treeiter)
                
            self.del_cache_simple(bookmark.name)
           
            
    def on_filter_by_changed(self, editable : Gtk.Editable):
        self.filter_by_filter.refilter()
        
        
    def refresh_title(self):
        title = None
            
        if self.has_changed() == True:
            title = self.get_title_changed()
        else:
            title = self.get_title()
        
        self.window.set_title(title)

        self.last_title_refresh = time.time()
   
   
    def filter_by_function(self, model : Gtk.TreeModel, treeiter : Gtk.TreeIter, data):
        """
        This method is used by self.filter_by_filter to filter the values of
        self.tree_model
        """
        display = False
       
        bookmark = None
        if treeiter is not None:
            bookmark = self.tree_row_to_bookmark(model[treeiter])
            bookmark = self.get_cache(bookmark.name)
        
        if bookmark != None:
            filter_by_text = self.filter_by_entry.get_text()
            
            for keyword in filter_by_text.split(' '):
                display = bookmark.fuzzy_search(keyword)
                
                if display == False:
                    break
                
        return display
    
            
    def on_row_doubleclicked(self, tree_view : Gtk.TreeView,
                             tree_path : Gtk.TreePath, tree_column : Gtk.TreeViewColumn):
        bookmark = None
        model, treeiter = self.tree_selection.get_selected()
        if treeiter is not None:
            bookmark = self.tree_row_to_bookmark(model[treeiter])
            bookmark = self.get_cache(bookmark.name)

        if bookmark != None:
            execute = CONFIG_SINGLETON.get_config()["Preferences"]["Doubleclick_Execute"]
            
            if bookmark.open_with is not None and bookmark.open_with != '':
                execute = bookmark.open_with
                
            os.spawnvpe(os.P_NOWAIT, execute, [ execute, bookmark.url ], os.environ)
            
    
    def on_selection_changed(self, selection : Gtk.TreeSelection):
        model, treeiter = self.tree_selection.get_selected()
        if treeiter is not None:
            bookmark = self.tree_row_to_bookmark(model[treeiter])
            bookmark = self.get_cache(bookmark.name)
            
            # Only update the cache for non-existing bookmarks
            if bookmark == None:
                bookmark = self.tree_row_to_bookmark(model[treeiter])
                self.update_cache(bookmark)
           
            self.bookmark_to_edit(bookmark, self.name_entry, self.url_entry,
                                  self.tags_entry, self.open_with_entry,
                                  self.description_textview)
            self.detail_ok_button.set_sensitive(True)
        else:
            bookmark = Bookmark(name = '',
                                url = '',
                                description = '')
            self.bookmark_to_edit(bookmark, self.name_entry, self.url_entry,
                                  self.tags_entry, self.open_with_entry,
                                  self.description_textview)
            self.detail_ok_button.set_sensitive(False)

            
    def on_ok_clicked(self, button : Gtk.Button):
        model, treeiter = self.tree_selection.get_selected()
        if treeiter is not None:
            old_bookmark = self.tree_row_to_bookmark(model[treeiter])
            bookmark = self.edit_to_bookmark(self.name_entry, self.url_entry, 
                                             self.tags_entry, self.open_with_entry,
                                             self.description_textview)
            self.bookmark_to_tree_row(bookmark, model[treeiter])
            self.update_cache(bookmark, old_name = old_bookmark.name)
            
            self.filter_by_filter.refilter()
        else:
            # This should not happen, please see self.on_selection_changed
            dialog = Gtk.MessageDialog(text = 'Please select a bookmark first!',
                                   type = Gtk.MessageType.WARNING,
                                   buttons = (Gtk.STOCK_OK, Gtk.ResponseType.OK))
            dialog.set_default_response(Gtk.ResponseType.NO)
            dialog.run()
            dialog.destroy()
            
            
    def write_database_failed_dialog(self, path):
        dialog = Gtk.MessageDialog(text = 'Writing the database to "' + path + '" failed!',
                                   type = Gtk.MessageType.ERROR,
                                   buttons = (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.run()
        dialog.destroy()
        
        
    def read_database_failed_dialog(self, path):
        dialog = Gtk.MessageDialog(text = 'Reading the database from "' + path + '" failed!',
                                   type = Gtk.MessageType.ERROR,
                                   buttons = (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.run()
        dialog.destroy()
        
    
    def check_changes_and_save(self):
        """
        Checks if any changes have been made to the data and suggest to save those changes.
        """
        if self.has_changed() == True:
            dialog = Gtk.MessageDialog(text = 'Save changes?',
                                       type = Gtk.MessageType.WARNING,
                                       buttons = (Gtk.STOCK_YES, Gtk.ResponseType.YES,
                                                  Gtk.STOCK_NO, Gtk.ResponseType.NO))
            dialog.set_default_response(Gtk.ResponseType.YES)
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.YES:
                self.on_save_as(None)
            
 
            
    def bookmark_to_edit(self, bookmark, name_entry : Gtk.Entry, url_entry : Gtk.Entry, 
                         tags_entry : Gtk.Entry, open_with_entry : Gtk.Entry,
                         description_textview : Gtk.TextView):
        """
        Convert a bookmark to input values
        """
        
        tags_text = ''
       
        i = 1 
        for tag in bookmark.tags:
            if i > 1:
                tags_text = tags_text + MainWindow.TAGS_SEPARATOR 
            
            tags_text = tags_text + tag.name
            
            i = i + 1

        description_buffer = description_textview.get_buffer()
        description = bookmark.description
        if description == None:
            description = ""
        
        name_entry.set_text(bookmark.name)
        url_entry.set_text(bookmark.url)
        tags_entry.set_text(tags_text)
        open_with_entry.set_text(bookmark.open_with)
        description_buffer.set_text(description)
    
    
    def edit_to_bookmark(self, name_entry : Gtk.Entry, url_entry : Gtk.Entry,
                         tags_entry : Gtk.Entry, open_with_entry : Gtk.Entry,
                         description_textview : Gtk.TextView):
        """
        Convert the input values to a bookmark
        """
        
        tags = [ ]
        tags_text = tags_entry.get_text()
        for tag_text in tags_text.split(MainWindow.TAGS_SEPARATOR):
            tag = None
            for current_bookmark in self.current_bookmarks:
                for current_tag in current_bookmark.tags:
                    if current_tag.name == tag_text:
                        tag = current_tag
                        break
                
                if tag != None:
                    break
            
            if tag == None:
                tag = Tag(name = tag_text)
           
            tags.append(tag)
       
        description_buffer = description_textview.get_buffer()
        start_iter = description_buffer.get_start_iter()
        end_iter = description_buffer.get_end_iter()
        description = description_buffer.get_text(start_iter, 
                                                  end_iter, 
                                                  True)
        
        bookmark = Bookmark(name = name_entry.get_text(),
                            url = url_entry.get_text(),
                            open_with = open_with_entry.get_text(),
                            description = description,
                            tags = tags)
        
        return bookmark
    
            
    def bookmark_to_tree_row(self, bookmark : Bookmark, row : Gtk.TreeModelRow):
        """
        Sets the values of bookmark onto row.
        """
        row[0] = bookmark.name
        row[1] = bookmark.url
   
    
    def tree_row_to_bookmark(self, row : Gtk.TreeModelRow):
        """
        Returns a Bookmark object for the row.
        """
        name = row[0]
        url = row[1]
       
        bookmark = Bookmark(name  = name,
                            url = url,
                            description = '',
                            open_with = '') 
        
        return bookmark
        
            
    def tree_to_bookmarks(self, tree_model : Gtk.TreeStore):
        """
        Returns the tree as an array of Bookmark
        """
        
        ret = []
        
        for row in tree_model:
            ret.append(self.tree_row_to_bookmark(row))
        
        return ret
    
    
    def bookmarks_to_tree(self, bookmarks, tree_model : Gtk.TreeStore):
        for bookmark in bookmarks:
            row = ( bookmark.name, bookmark.url )
            tree_model.append(None, row) 
            
        
    def get_cache(self, name : str):
        """
        Returns a Bookmark or None
        """
        for current_bookmark in self.current_bookmarks:
            if current_bookmark.name == name:
                return current_bookmark
            
        return None
    
    
    def update_cache(self, bookmark : Bookmark, old_name = None, refresh_title = True):
        '''
        Returns 
        - 1 if @bookmark was added. 
        - 2 if the corresponding cached bookmark was updated by @bookmark.
        - < 0 if an error occured.
        '''
        
        ret = -1
        
        name = bookmark.name
        if old_name is not None:
            name = old_name
            
        current_bookmark = self.get_cache(name)
                
        if current_bookmark == None:
            self.current_bookmarks.append(bookmark) 
            ret = 1
        else:
            current_bookmark.copy(bookmark)
            ret = 2
            
        if refresh_title == True and ret > 0:
            self.refresh_title()
            
        return ret
            
    
    def del_cache_simple(self, name : str):
        i = 0
       
        while i < len(self.current_bookmarks):
            current_bookmark = self.current_bookmarks[i]
            if current_bookmark.name == name:
                del self.current_bookmarks[i]
                break
            i = i + 1
            
        self.refresh_title()

            
    def read_and_use_database(self):
        """
        Reads the contents of the database and place those contents in the variables
        for the GUI.
        
        Returns:
        - 0 if everything went alright. 
        - 1 if the passed file cannot be read
        """
        path = self.get_path()
        ret = 0

        if DATABASE_SINGLETON.open_database(path) == 0:
            session = DATABASE_SINGLETON.get_session()
                
            db_bookmarks = session.query(Bookmark).all()
            bookmarks = [ ]
                
            # Add bookmarks to cache
            for db_bookmark in db_bookmarks:
                bookmark = Bookmark()
                bookmark.copy(db_bookmark)
                bookmarks.append(bookmark)
           
            DATABASE_SINGLETON.close_database()
       
            for bookmark in bookmarks: 
                self.update_cache(bookmark, refresh_title = False) 
        
            self.bookmarks_to_tree(bookmarks, self.tree_model)
        else:
            ret = 1
        
        self.filter_by_filter.refilter()
        
        return ret

            
    def write_database(self):
        """
        Writes the displayed contents to the database.
        
        Returns:
        - 0 : Database was successfully written to the disk
        - 1 : Some error happened
        """
        if self.get_path() is not None and os.path.isfile(self.get_path()):
            autobackup = True
            autobackup_suffix = '~'
            try:
                autobackup = CONFIG_SINGLETON.get_config()["Preferences"]["Autobackup"]
                autobackup_suffix = CONFIG_SINGLETON.get_config()["Preferences"]["Autobackup_Suffix"]
            except:
                pass
                
            if autobackup == True:
                os.rename(self.get_path(), 
                          self.get_path() + autobackup_suffix)
            else:
                os.remove(self.get_path())
                
                
        ret = 0
       
        try: 
            DATABASE_SINGLETON.open_database(self.get_path())
            session = DATABASE_SINGLETON.get_session()
        
          
            bookmarks_to_add = [ ]
            for bookmark in self.current_bookmarks:
                bookmark_to_add = Bookmark()
                bookmark_to_add.copy(bookmark)
       
                bookmark_to_add_tags = bookmark_to_add.tags 
                bookmark_to_add.tags = self.write_database_tags(bookmark_to_add_tags, session)
                
                bookmarks_to_add.append(bookmark_to_add)
                   
            
            for bookmark_to_add in bookmarks_to_add: 
                session.add(bookmark_to_add)
        
            session.commit()
            
            DATABASE_SINGLETON.close_database()
            
        except Exception as e:
            ret = 1
            print(e)
            
        return ret
        
    def write_database_tags(self, tags, session):
        """
        Returns the db associated tags.
        """
        updated_tags = [ ]
        
        for tag in tags:
            tag_to_add = None
            db_tags = session.query(Tag).filter(Tag.name == tag.name).all()
            if len(db_tags) > 0:
                db_tag = db_tags[0]
                
                tag_to_add = db_tag
            else:
                tag_to_add = tag
                del tag.id
               
            session.add(tag_to_add)
            session.commit()
            updated_tags.append(tag_to_add)
            
        return updated_tags
