#! /usr/bin/env python
# -*- coding: UTF-8 -*-

<<<<<<< HEAD
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


=======
>>>>>>> origin/master
import os
import sys

import cgi
import cgitb

import creoleparser
import jinja2


#===============================================================================
# Configuration
#===============================================================================

# The base path of the pyco installation 
base_path = '/home/dustin/workspaces/private/pyco/pyco'

# The name of the script
base_name = 'index.py'
  
# The base bath of the pages tree
pages_path = base_path + '/pages'
  
# The base path of the template
template_path = base_path + '/template'

# The name of the template
template_name = 'main.html'

# The title of the web site
site_title = 'PyCo Test'

# Enable CGI debug output
cgitb.enable()


#===============================================================================
<<<<<<< HEAD
# Returns the pages on a given path
#===============================================================================
def getSubPages(path):
  # Make real path from path
  real_path = realPath(path)
  
  # Check if file is directory
  if not os.path.isdir(real_path):
    return None
  
  # Get list of file system entries in path
  list = os.listdir(real_path)
  
  # Build list of sub pages
  childs = []
  for l in list:
    # Make real path from path
    real_path = realPath(path + '/' + l)
    
    # Check if file is hidden
    if l.startswith('.') or l == '404':
      continue
    
    # Check if file is directory, link or regular file
    if not (os.path.isdir(real_path) or 
            os.path.islink(real_path) or 
            os.path.isfile(real_path)):
      continue
    
    # Add to list of valid child
    if path != '/':
      childs.append(path + '/' + l)
    else:
      childs.append('/' + l)
  
  return childs


#===============================================================================
# Splits the path into path parts
#===============================================================================
def splitPath(path):
  return path.split('/')


#===============================================================================
# Returns the real path for the given path 
#===============================================================================
def realPath(path):
  return os.path.normpath(pages_path + '/' + path)


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
    # Get target of link
    link = os.path.normpath('/' + os.readlink(real_path))
    
    # Resolve link recursive
    return resolvePath(link)
  
  # Check if file is directory
  if os.path.isdir(real_path):
    return resolvePath(path + '/.content')
  
  # Check if file is normal file
  if os.path.isfile(real_path):
    return path
  
  # File is something else
  return None
    

#===============================================================================
# Main function
#===============================================================================
if __name__ == '__main__':
  
  # Send HTTP content type
  print 'Content-Type: text/html;charset=utf-8'
  
  # Get requested path
  if os.environ.has_key('PATH_INFO'):
    path = os.environ['PATH_INFO']
  else:
    path = '/'
  
  # Get resolved path
  resolved_path = resolvePath(path)
  
  # Check if path exits or redirect to 404
  if not resolved_path:
    # Send HTTP status
    print 'HTTP/1.1 404 Not Found'
    
    # Set path to 404 page
    path = '/404'
    resolved_path = resolvePath(path)  
  
  # Send HTTP header finished
  print ''
  
  # Handle missing error pages
  if not resolved_path:
    print '404 - Not Found'
    sys.exit()
    
  # Get real path of page and read content
  file = open(realPath(resolved_path))
  content = file.read()
  file.close()
  
  # Create HTML from file
  html_content = creoleparser.creole2html(content)
  
  # Load template
  template_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path));
  template = template_env.get_template(template_name)
  
  # Render template
  output = template.render(content = html_content,
                           path = path,
                           resolved_path = resolved_path,
                           site_title = site_title,
                           base_name = base_name,
                           path_parts = path.split('/')[1:],
                           resolved_path_parts = resolved_path.split('/')[1:],
                           getSubPages = getSubPages,
                           splitPath = splitPath
  )
  
  # Print template output
  print output.encode('ASCII')
  
  