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

# The page content is written using creole syntax. the creole syntax is the
# commonly known as wiki-syntax. This allows to write and edit page content using
# every text editor in an easy to learn syntax. For further information about
# creole see <http://www.wikicreole.org/>.


def renderCreole(content):
  # Create creole parser to parse file to HTML
  creole_dialect = creoleparser.dialects.create_dialect(creoleparser.dialects.creole11_base,
                                                        wiki_links_base_url = '/' + settings['base_name'] + '/',
                                                        wiki_links_class_func = None,
                                                        macro_func = None,
                                                        indent_class = None)
  
  creole_parser = creoleparser.Parser(creole_dialect,
                                      encoding = 'utf-8')
  
  # Create HTML from file
  return unicode(creole_parser(content), 
                 encoding = 'utf-8')

renderers['creole'] = renderCreole
