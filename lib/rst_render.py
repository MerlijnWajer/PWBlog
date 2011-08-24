#!/usr/bin/python

# :Author: David Goodger, the Pygments team, Guenter Milde. Modified by Merlijn Wajer
# :Date: $Date: $
# :Copyright: This module has been placed in the public domain.

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_string, publish_parts, default_description

description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources. Uses `pygments` to colorize the content of'
               '"code-block" directives. Needs an adapted stylesheet' 
               + default_description)

# Define a new directive `code-block` that uses the `pygments` source
# highlighter to render code in color. 
#
# Code from the `pygments`_ documentation for `Using Pygments in ReST
# documents`_.

from docutils import nodes
from docutils.parsers.rst import directives
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

pygments_formatter = HtmlFormatter()

def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        # no lexer found - use the text one instead of an exception
        lexer = get_lexer_by_name('text')
    parsed = highlight(u'\n'.join(content), lexer, pygments_formatter)
    return [nodes.raw('', parsed, format='html')]
pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
directives.register_directive('code-block', pygments_directive)


import time

# Call the docutils publisher to render the input as html::
def render_rst(rst_str):
    overrides = {'stylesheet_path': 'static/pygments-default.css',
                 'link_stylesheet': 'True'}

    t = time.time()

    o = publish_parts(rst_str, writer_name='html', settings_overrides=overrides)

    t2 = time.time()
    print 'Time:', t2-t

    return o
