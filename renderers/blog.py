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

# Renders the pictures in the given folder into a picture gallery using
# smoothgallery. The configuration of the gallery has the following format:
# {
#   "id" : "$ID$",
#   "path" : "$PATH$"
# }
#
# The $ID$ must be a unique id for the gallery. The path contains the pictures.
# Additional to the pictures the given path must contain the two folders
# "smalls" and "thumbs".
#
# The folder "smalls" must contain a smaller variant of the pictures with the
# same filename and a size of 800x600 pixels.
#
# The "thumbs" fulder must contain a smaller variant of the pictures with the
# same filename and a sizeo of 100x75 pixels.


import simplejson as json

def renderBlog(content):
  # Parse the posts
  blog = json.loads(content)
  
  # Build blog page
  output = ''
  output += '<ol class="blog">'

  for post in blog['posts']:
    output += '<li class="blog">'
    
    output += '<p class="info">'
    output += post['autor']
    output += '@'
    output += post['date']
    output += '</p>'
    
    output += '<h2>'
    output += post['titel']
    output += '</h2>'
    
    if post['renderer'] in renderers:
      renderer = renderers[post['renderer']]
    else:
      renderer = renderers[None]
    
    filename = os.path.normpath(settings['base_path'] + '/' + blog['path'] + '/' + post['file'])

    file = codecs.open(filename,
                       encoding='utf-8')
    content = ''.join(file.readlines())
    file.close()
    
    output += renderer(content)
    
    output += '</ li>'
    
  output += '</ol>'
   
  return output

renderers['blog'] = renderBlog
