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
