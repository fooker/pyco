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

def renderSmoothgallery(content):
  # Parse module configuration
  config = json.loads(content)
  
	# Find list of images
  files = os.listdir(os.path.normpath(settings['base_path'] + '/' + config['path']))
   
  # Build galary page
  output = ''
  output += '<script src="/smoothgallery/scripts/mootools.v1.11.js" type="text/javascript"></script>'
  output += '<script src="/smoothgallery/scripts/jd.gallery.js" type="text/javascript"></script>'
  output += '<link rel="stylesheet" href="/smoothgallery/css/jd.gallery.css" type="text/css" media="screen" />'
  
  output += '<div id="' + config['id'] + '">'
  for filename in files:
    if not os.path.isdir(os.path.normpath(settings['base_path'] + '/' + config['path'] + '/' + filename)):
      path_real = os.path.normpath(settings['base_path'] + '/' + config['path'] + '/' + filename)
      path_image = os.path.normpath(config['path'] + '/' + filename)
      path_thumb_real = os.path.normpath(settings['base_path'] + '/' + config['path'] + '/thumbs/' + filename)
      path_thumb_image = os.path.normpath(config['path'] + '/thumbs/' + filename)
      path_small_real = os.path.normpath(settings['base_path'] + '/' + config['path'] + '/smalls/' + filename)
      path_small_image = os.path.normpath(config['path'] + '/smalls/' + filename)
      
      output += '<div class="imageElement">'
      output += '<h3>' + filename + '</h3>'
      output += '<p></p>'
      output += '<a href="' + path_image + '" title="open image" class="open"></a>'
      output += '<img src="' + path_small_image + '" class="full" />'
      output += '<img src="' + path_thumb_image + '" class="thumbnail" />'
      output += '</div>'
  
  output += '</div>'
  
  output += '<script type="text/javascript">'
  output += 'function startGallery() {'
  output += 'var ' + config['id'] + ' = new gallery($(\'' + config['id'] + '\'), {'
  output += 'timed: false'
  output += '});'
  output += '}'
  output += 'window.addEvent(\'domready\', startGallery);'
  output += '</script>'
   
  return output

renderers['smoothgallery'] = renderSmoothgallery
