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
from distutils.core import setup

setup(
    name = "bookman",
    version = "0.5",
    author = "Richard Paul Baeck",
    author_email = "richard.baeck@free-your-pc.com",
    license = "MIT",
    description = ("A tool to manage your bookmarks."),
    long_description = open("README.md").read(),
    packages = [ "bookman",
                 "bookman.models"],
    scripts = [ "bookman-gui" ],
    data_files = [ ( "share/bookman",
                    [ "config.yaml" ] ),
                   ( "share/bookman/ui",
                    [ "ui/main_window.glade",
                      "ui/preferences_dialog.glade" ] ),
                   
                   ( 'share/applications',
                     [ 'bookman.desktop' ] ),
                   
                   ( "share/locale/de/LC_MESSAGES",
                    [ "locale/de/LC_MESSAGES/bookman.mo" ] ),
                   
                   ("share/locale/en/LC_MESSAGES",
                    ["locale/en/LC_MESSAGES/bookman.mo"] ) 
                 ],
    install_requires = [ "SQLAlchemy", "PyYAML" ]
)
