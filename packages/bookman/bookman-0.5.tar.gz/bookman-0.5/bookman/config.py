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

from enum import Enum
import sys
import os
import copy

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class FileMode(Enum):
    DEVELOPMENT = 1
    PRODUCTION_USER = 2
    PRODUCTION_LOCAL = 3
    PRODUCTION_SYSTEM = 4
    

class Config():
    CONFIG_BASENAME = 'config.yaml'
    
    PATH_TRIES = [ (os.environ["HOME"] + '/.bookman', FileMode.PRODUCTION_USER ),
                   ('.', FileMode.DEVELOPMENT),
                   ('/usr/local/share/bookman', FileMode.PRODUCTION_LOCAL),
                   ('/usr/share/bookman', FileMode.PRODUCTION_SYSTEM) ]
    

    def __init__(self):
        self.config = None
        self.full_config = None
        self.development_mode = False
        
        self.reload_config()
        
            
    def reload_config(self):
        """
        Reinitializes the object with a config file.
        
        Returns True if reloading was successful and False otherwise.
        """
        successful_reload = False
        
        self.development_mode = False

        path_tuple = self.try_paths(Config.CONFIG_BASENAME)
        if path_tuple != None:
            config_filename = path_tuple[0]
            
            if path_tuple[1] == FileMode.DEVELOPMENT:
                self.development_mode = True
            else:
                self.development_mode = False
    
            with open(config_filename, 'r') as file:
                self.full_config = load(file, Loader = Loader)
    
            if self.development_mode == False:
                self.set_config(copy.deepcopy(self.full_config["Environment"]["Production"]))
            else:
                self.set_config(copy.deepcopy(self.full_config["Environment"]["Development"]))
                
            successful_reload = True
            
        return successful_reload
            
        
    def try_paths(self, basename):
        """
        Returns a tuple with:
        1. The absolute filename for the basename
        2. The FileMode
        """
        ret_tuple = None
        
        for dirname in Config.PATH_TRIES:
            filename = dirname[0] + '/' + basename
            if os.path.isfile(filename):
                ret_tuple = (filename, dirname[1])
                break
            
        return ret_tuple
            
  
    def get_absolute_path(self, basename):
        return self.try_paths(basename)[0]
    
    
    def get_try_paths_dirname(self, file_mode : FileMode):
        for dirname in Config.PATH_TRIES:
            if dirname[1] == file_mode:
                return dirname[0]


    def get_config(self):
        return self.config
    
    
    def set_config(self, config):
        self.config = config
   
    
    def write_config_local(self):
        full_config = copy.deepcopy(self.full_config)
        full_config["Environment"]["Production"] = copy.deepcopy(self.get_config())
        
        config_dirname = self.get_try_paths_dirname(FileMode.PRODUCTION_USER)
        config_filename = config_dirname + '/' + Config.CONFIG_BASENAME
        
        if os.path.isdir(config_dirname) == False:
            os.mkdir(config_dirname)
        
        with open(config_filename, 'w') as file:
            dump(full_config, file) 


CONFIG_SINGLETON = Config()
