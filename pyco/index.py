#! /usr/bin/env python
# -*- coding: UTF-8 -*-

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
  
# The base bath of the pages tree
pages_path = base_path + '/pages'
  
# The base path of the template
template_path = base_path + '/template'

# The name of the template
template_name = 'main.html'

# Enable CGI debug output
cgitb.enable()


#===============================================================================
# Returns the real path for the given path 
#===============================================================================
def realPath(path):
  return os.path.normpath(pages_path + path)


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
  output = template.render(path = path,
                           resolved_path = resolved_path,
                           content = html_content)
  
  # Print template output
  print output.encode('ASCII')
  
  