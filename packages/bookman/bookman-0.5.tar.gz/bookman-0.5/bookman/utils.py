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

from html.parser import HTMLParser

from bookman.models import Tag
from bookman.models import Bookmark

class Transformator():
    def __init__(self):
        pass
    
    
    def get_bookmarks(self) -> [ ]:
        pass
    
    

class FirefoxBookmarkHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.init()
        
        
    def init(self):
        self.current_bookmark = None
        self.current_is_link = False
        self.current_is_folder_name = False
        self.current_tag = None
        self.current_tags = [ ]
        self.current_url = None
        self.bookmarks = [ ]

    
    def feed(self, data):
        self.init()
        HTMLParser.feed(self, data)
        
    
    def get_bookmarks(self) -> [ ]:
        return self.bookmarks
    
    
    def FolderBegin(self, tag, attrs):
        pass
    
   
    def FolderEnd(self, tag):
        if len(self.current_tags) > 0:
            self.current_tags.pop()
        
 
    def FolderNameBegin(self, tag, attrs):
        self.current_is_folder_name = True
        
    
    def LinkBegin(self, tag, attrs):
        self.current_is_link = True
        
        for attr in attrs:
            if attr[0] == 'href':
                self.current_url = attr[1]
        
    
    def handle_starttag(self, tag, attrs):
        switch = {
            'dl' : self.FolderBegin,
            'h3' : self.FolderNameBegin,
            'a' : self.LinkBegin
        }
        
        method = switch.get(tag)
        if method is not None:
            method(tag, attrs)
        
        
    def handle_endtag(self, tag):
        if self.current_is_link == True:
            self.current_is_link = False
            
        if self.current_is_folder_name == True:
            self.current_is_folder_name = False
            
        switch = {
            'dl' : self.FolderEnd,
        }
        
        method = switch.get(tag)
        if method is not None:
            method(tag)
        
        
    def handle_data(self, data):
        if self.current_is_folder_name == True:
            # TODO: create Tag
            tag_name = data.replace(" ", "").replace("\t", "")
            self.current_tag = Tag(name = tag_name)
            
            self.current_tags.append(self.current_tag)

        if self.current_is_link == True:
            bookmark_name = data
            self.current_bookmark = Bookmark(name = bookmark_name,
                                             url = self.current_url,
                                             tags = self.current_tags,
                                             description = '')
            self.bookmarks.append(self.current_bookmark)
            

class FirefoxBookmarkTransformator(Transformator):
    def __init__(self, filename):
        self.filename = None
        
        self.filename = filename
        
        
    def doc_to_bookmark(self, doc) -> [ ]:
        bookmarks = [ ]
        
        if doc["@href"] is not None:
            url = doc["@href"] 
        else:
            pass 
       
        return bookmarks
        
        
    def get_bookmarks(self) -> [ ]:
        doc = None
        
        with open(self.get_filename(), 'r') as fd:
            doc = fd.read()
            
        parser = FirefoxBookmarkHTMLParser()
        parser.feed(doc)
        bookmarks = parser.get_bookmarks()
       
        return bookmarks
    
    
    def get_filename(self) -> str:
        return self.filename
    
    