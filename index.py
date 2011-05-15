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

import os
import sys
import xattr

import codecs
import re

import cgi
import cgitb

import creoleparser
import jinja2


#===============================================================================
# Configuration
#===============================================================================

# Enable CGI debug output
cgitb.enable()

# The settings container
settings = {}

# The base path of the pyco installation 
settings['base_path'] = '/var/www/'

# The name of the script
settings['base_name'] = 'index.py'

# The title of the web site
settings['site_title'] = 'PyCo'
  
# The base bath of the pages tree
settings['pages_path'] = settings['base_path'] + '/pages'

# Define special pages
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


#===============================================================================
# Plugin to display raw content
#===============================================================================
def renderNone(content):
  # Enclose the content with '<pre>' tags
  return '<pre>' + content + '</pre>'


#===============================================================================
# Returns the pages on a given path
#===============================================================================
def getSubPages(path):
  # Make real path from path
  real_path = realPath(path)
  
  # Check if file is directory
  if not os.path.isdir(real_path):
    return []
  
  # Get list of file system entries in path
  list = os.listdir(real_path)
  
  # Check if order file exists and read it into order list
  order_list = []
  if settings['pages_order_file'] and os.path.exists(real_path + '/' + settings['pages_order_file']):
    for l in open(real_path + '/' + settings['pages_order_file']):
      order_list.append(l[:-1])

  # Build list of sub pages
  childs = []
  for l in list:
    # Make real path from path
    real_path = realPath(os.path.normpath(path + '/' + l))
    
    # Build full path
    if path != '/':
      full_path = os.path.normpath(path + '/' + l)
      
    else:
      full_path = os.path.normpath('/' + l)
    
    # Check if file is hidden
    if l.startswith('.'):
      continue
    
    # Check if file should be ignored
    if full_path in settings['pages_ignored']:
      continue
    
    # Check if file is directory, link or regular file
    if not (os.path.isdir(real_path) or 
            os.path.islink(real_path) or 
            os.path.isfile(real_path)):
      continue
   
    # Calculate item ordering
    if order_list.count(l):
      # Use ordering from order file
      order = order_list.index(l)
      
    else:
      # Get order from extended file attributes or set int to maximum of integer
      # if no such attribute exits
      xattrs = xattr.xattr(real_path)
      if settings['pages_order_xattr'] in xattrs:
        order = int(xattrs[settings['pages_order_xattr']])
      else:
        order = sys.maxint

    # Add path and order to list of valid child
    childs.append((full_path, order))
  
  # Sort childs by order
  childs.sort(key = lambda child: child[1])
  
  # Return list of sub pages
  return [child[0] for child in childs]


#===============================================================================
# Splits the path into path parts
#===============================================================================
def splitPath(path):
  return path.split('/')[1:]


#===============================================================================
# Joins the parts to a path
#===============================================================================
def joinPath(parts):
  return '/' + ('/'.join(parts))


#===============================================================================
# Returns a sub path
#
# The returned path is the parent path of the given path starting
# at root and ending at the given level
#===============================================================================
def subPath(path, level):
	return joinPath(splitPath(path)[0:level])


#===============================================================================
# Returns the name of the page of the path
#
# It fetches the last part of splitPath(path), replaces the underscores with
# spaces and removes the order number.
#===============================================================================
def getName(path):
  page_path = splitPath(path)[-1];
  return page_path


#===============================================================================
# Returns the real path for the given path 
#===============================================================================
def realPath(path):
  return os.path.normpath(settings['pages_path'] + path)


#===============================================================================
# Returns the pretty path for the given path
#===============================================================================
def prettyPath(path):
  parts = splitPath(path)
  if parts[-1] == '.page':
    return joinPath(parts[:-1])
  else:
    return joinPath(parts)


#===============================================================================
# Resolve the given path
#===============================================================================
def resolvePath(path):
  # Make real path from path
  real_path = realPath(path)
  
  # Check if file exists
  if not os.path.exists(real_path):
    return None
  
  # Check if file is readable
  if not os.access(real_path, os.R_OK):
    return None
  
  # Check if file is link
  if os.path.islink(real_path):
    # Get base path
    base_path = os.path.dirname(path)
    
    # Get target of link
    link = os.path.normpath(base_path + '/' + os.readlink(real_path))
    
    # Resolve link recursive
    return resolvePath(link)
  
  # Check if file is directory
  if os.path.isdir(real_path):
    return resolvePath(os.path.normpath(path + '/.page'))
  
  # Check if file is normal file
  if os.path.isfile(real_path):
    return path
  
  # File is something else
  return None


#===============================================================================
# Parses the shi bang
#===============================================================================
def parseShiBang(shi_bang):
  result = re.match('^#! *([\w]*) *$', shi_bang)
  
  if result != None:
    return result.group(1)
  else:
    return None


#===============================================================================
# Main function
#===============================================================================
if __name__ == '__main__':

  # Send HTTP content type
  print 'Content-Type: text/html;charset=utf-8'  
  
  # Build renderers map and add the 'none' renderer
  renderers = {}
  renderers[None] = renderNone
  
  # Load other renderers from plugin folder
  sys.path.insert(0, settings['renderers_path'])
  for renderer_file in os.listdir(settings['renderers_path']):
    if renderer_file.endswith('.py'):
      renderer_module = execfile(os.path.join(settings['renderers_path'], renderer_file))
   
  # Build site context
  site = {}
  site['title'] = settings['site_title']
  site['base'] = settings['base_name']
  
  # Build function context
  pyco = {}
  pyco['splitPath'] = splitPath
  pyco['joinPath'] = joinPath
  pyco['subPath'] = subPath
  pyco['getName'] = getName
  pyco['getSubPages'] = getSubPages
  
  # Build page context
  page = {}
  
  # Get requested path
  if os.environ.has_key('PATH_INFO'):
    page['path_requested'] = os.environ['PATH_INFO']
    
  else:
    page['path_requested'] = '/'
  
  # Resolve requested path
  page['path_resolved'] = resolvePath(page['path_requested'])
  
  # Check if path exits and redirect to 404 if not
  if not page['path_resolved']:
    # Set path to 404 page
    page['path_resolved'] = resolvePath(settings['pages_special']['not_found'])
    
  # Send HTTP header finished
  print ''
  
  # Handle missing pages
  if not page['path_resolved']:
    print '404 - Not Found'
    sys.exit()
  
  # Get title of page
  page['title'] = splitPath(page['path_resolved'])[-1]
  
  # Get real path of page
  page['path_real'] = realPath(page['path_resolved'])
 
  # Get the pretty path
  page['path'] = prettyPath(page['path_resolved']);
 
  # Read shi bang and raw content of page
  file = codecs.open(page['path_real'],
                     encoding='utf-8')
  page['content_all'] = file.readlines()
  file.close()
  
  # Extract and parse shi bang
  page['shi_bang'] = parseShiBang(page['content_all'][0])
  
  # Get content without shi bang if shi bang is valid or the full content otherwise
  if page['shi_bang'] != None and page['shi_bang'] in renderers:
    page['content_raw'] = ''.join(page['content_all'][1:])
  else:
    page['content_raw'] = ''.join(page['content_all'])
   
  # Find renderer for shi bang
  if page['shi_bang'] in renderers:
    page['renderer'] = renderers[page['shi_bang']]
  else:
    page['renderer'] = renderers[None]
  
  # Render content using found renderer
  page['content'] = page['renderer'](page['content_raw'])
  
  # Load template
  jinja2_loader = jinja2.FileSystemLoader(settings['template_path'],
                                          encoding = 'utf-8')
  jinja2_env = jinja2.Environment(loader = jinja2_loader);
  jinja2_template = jinja2_env.get_template(settings['template_name'])
  
  # Render template
  jinja2_output = jinja2_template.render(pyco = pyco,
                                         site = site,
                                         page = page,
                                         content = page['content'])
  
  # Print template output
  print jinja2_output.encode('utf-8')
  
  
