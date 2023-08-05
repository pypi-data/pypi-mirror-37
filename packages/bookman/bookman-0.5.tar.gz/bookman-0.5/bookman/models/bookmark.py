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
import re

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref

from . import Base
from . import Folder
from . import Tag

BOOKMARK_TAG_LINK_TABLE = Table('bookmark_tag_link', Base.metadata,
    Column('bookmark_id', Integer, ForeignKey('bookmark.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Bookmark(Base):
    __tablename__ = 'bookmark'
    
    id = Column(Integer, primary_key = True)
    
    name = Column(String(250), nullable = False)
    
    url = Column(String(250), nullable = False)
    
    open_with = Column(String(1024), nullable = False)
    
    description = Column(String(99999), nullable = False)

    folder_id = Column(Integer, ForeignKey('folder.id'))
    # folder = relationship(
    #     Folder,
    #    backref = backref('folders',
    #                      uselist=True,
    #                      cascade='delete,all')) 
    
    tags = relationship("Tag", secondary = BOOKMARK_TAG_LINK_TABLE,
                        lazy = 'joined')
    
 
    def copy(self, other):
        self.id = other.id
        self.name = other.name
        self.url = other.url
        self.open_with = other.open_with
        self.description = other.description
       
        self.tags = [ ] 
        for other_tag in other.tags:
            tag = Tag(name = '')
            tag.copy(other_tag)
            self.tags.append(tag)
        
        
    def fuzzy_search(self, keyword : str):
        """
        Returns True if keyword is in any value of this Bookmark. Returns False otherwise.
        """
        matches = False
       
        if keyword is None or len(keyword) == 0:
            matches = True
        elif keyword[0] == '#':
            search_for_tag = keyword[1 : ]
            for tag in self.tags:
                if tag.name == search_for_tag:
                    matches = True
                    break
        else:
            regex = re.compile(keyword) 
            if regex.search(self.name) or regex.search(self.url) or regex.search(self.description):
                matches = True
                
        return matches
        
