#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# This file is part of PyCo.
# 
# PyCo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyCo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PyCo.  If not, see <http://www.gnu.org/licenses/>.

# The base path of the pyco installation where the index.py and this file are
# located.
settings['base_path'] = '/var/www/'

# The name of the PyCo script.
settings['base_name'] = 'index.py'

# The title of the web site used by the template to define the page title.
settings['site_title'] = 'PyCo'
  
# The base bath of the pages tree. All sub folders and file in this directory
# will be handled as items of the page.
settings['pages_path'] = settings['base_path'] + '/pages'

# Define specail pages. These pages have some special functions:
# not_found - the error page used for wrong links
settings['pages_special'] = {}
settings['pages_special']['not_found'] = '/404'

# The name of the order filed of extended file attributes
# In most cases the name should be prefixed by 'user.'
settings['pages_order_xattr'] = 'user.pyco.order'

# The name of the file defining the order. If no order field should be used, it
# can be left None. If the file exists in a sub-directory, it will disable
# xattr ordering.
settings['pages_order_file'] = None

# Set of pages ignored in trees, listings, etc...
settings['pages_ignored'] = []
settings['pages_ignored'].append(settings['pages_special']['not_found'])
settings['pages_ignored'].append(settings['pages_order_file'])
settings['pages_ignored'].append('/Impressum')

# The base path of the template
settings['template_path'] = settings['base_path'] + '/template'
  
# The name of the template
settings['template_name'] = 'main.html'

# The base path of the rendere plugins
settings['renderers_path'] = settings['base_path'] + '/renderers'

