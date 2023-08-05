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

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import Base

class DatabaseSingleton():
    session = None

    def open_database(self, path):
        '''Returns:
            - 0 : Connection has been established successfuly
            - 1 : File could not be opened
        '''
        ret = 0
        
        fullpath = 'sqlite:///' + path
        try:
            engine = create_engine(fullpath)
            Base.metadata.create_all(engine)
        except:
            ret = 1
       
        if ret == 0:
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            self.session = DBSession()
        
        return ret
        
    def close_database(self):
        self.get_session().expunge_all()
        self.get_session().close_all()
        Base.metadata.bind = None

    def get_session(self):
        return self.session

DATABASE_SINGLETON = DatabaseSingleton()
