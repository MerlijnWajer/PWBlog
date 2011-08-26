#!/usr/bin/env python

from jinja2 import Environment, PackageLoader

from lib.sessionhack import SessionHack, SessionHackException
from lib.webtool import WebTool

from lib.backend import make_backend
from lib.rst_render import render_rst
from lib.fsbackend import FSPWBlogBackend
from lib.sqlbackend import SQLPWBlogBackend

import datetime
import os
import mimetypes
import stat

USE_OWN_HTTPD = True
BASE_URL = ''
STATIC_URL = BASE_URL + '/static'

# HTML Allowed
BLOG_NAME = '''
<h1>Wizzup\'s Blog</h1>
<p> about:nonsense </p>
'''

def blogApp(env, start_response):

    r = wt.apply_rule(env['PATH_INFO'], env)

    # 404
    if r is None:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        tmpl = jinjaenv.get_template('404.html')

        return template_render(tmpl, env,
            {'url' : env['PATH_INFO']})

    elif type(r) in (tuple, list) and len(r) == 3:
        # Respond with custom headers
        start_response(r[0], r[1])
        r = r[2]

    # 200
    else:
        start_response('200 OK', [('Content-Type', 'text/html;charset=utf8')])

    # Response data

    # If r is not a file, but a string
    # prevent an exhausting loop
    if type(r) == str:
        return [r]

    return r

def template_render(template, env, vars):
    """
        Template Render is a helper that initialises basic template variables
        and handles unicode encoding.
    """
    vars['base_url'] = BASE_URL
    vars['static_url'] = STATIC_URL
    vars['blog_name'] = BLOG_NAME

    ret = unicode(template.render(vars)).encode('utf8')

    return ret

def error_page(env, error='No error?'):
    """
    Called on exceptions, when something goes wrong.
    """
    tmpl = jinjaenv.get_template('error.html')
    return template_render(tmpl, env, {'error' : error})

def blog_page(env, entry):
    if entry is None:

        o = backend.get_all_entries()

        if o:
            o = backend.lookup_entry(o[0].shortname)

        if not o:
            return None

    else:
        o = backend.lookup_entry(entry)
        if not o:
            return None

    related = backend.get_all_entries()
    related_page = backend_page.get_all_entries()
    categories = backend.get_all_categories()
    print categories

    tmpl = jinjaenv.get_template('main.html')

    return template_render(tmpl, env, {'post' : o,
            'categories' : categories,
            'related' : related, 'related_page' : related_page})

def page_page(env, entry):
    o = backend_page.lookup_entry(entry)
    if not o:
        return None

    related = backend.get_all_entries()
    related_page = backend_page.get_all_entries()
    categories = backend.get_all_categories()
    print categories

    tmpl = jinjaenv.get_template('main.html')

    return template_render(tmpl, env, {'post' : o,
            'categories' : categories,
            'related' : related, 'related_page' : related_page})

def main_page(env):
    return blog_page(env, entry=None)

def static_serve(env, static_file):
    """
    Serve static files ourselves. Most browsers will cache them after one
    request anyway, so there's not a lot of overhead.
    """
    mimetype = mimetypes.guess_type('./static/' + static_file)
    if mimetype[0] == None:
        return None

    blogpath = os.path.abspath(__file__)
    filepath = os.path.abspath('./static/' + static_file)
    blogdir =  os.path.dirname(blogpath) + '/static'

    if not filepath.startswith(blogdir):
        return None

    # print 'Serving static file:', static_file, 'with mime type:', mimetype[0]

    try:
        st = os.stat('./static/' + static_file)
        d = datetime.datetime.fromtimestamp(st[stat.ST_MTIME])

        headers = [('Content-Type', mimetype[0]),
                   ('Last-Modified', d.strftime('%a, %d %b %Y %H:%M:%S GMT'))
                   ]

        if 'HTTP_IF_MODIFIED_SINCE' in env:
            try:
                prev_date = datetime.datetime.strptime( \
                        env['HTTP_IF_MODIFIED_SINCE'], \
                        '%a, %d %b %Y %H:%M:%S GMT')
                if prev_date >= d:
                    return ['304 Not Modified', headers, '']
            except ValueError, e:
                pass

        f = open('./static/' + static_file)
        return ['200 OK', headers, f.read()]
    except (IOError, OSError):
        return None


if __name__ == '__main__':

    jinjaenv = Environment(loader=PackageLoader('pwblog', 'templates'))
    jinjaenv.autoescape = True
    wt = WebTool()

    backend = make_backend(SQLPWBlogBackend)

#    backend = make_backend(FSPWBlogBackend, path=\
#            os.path.dirname(os.path.abspath(__file__))+'/blogs/')

    backend_page = make_backend(FSPWBlogBackend, path=\
            os.path.dirname(os.path.abspath(__file__))+'/pages/')

    execfile('rules.py')


    app = blogApp
    app = SessionHack(app, error_page)


    if USE_OWN_HTTPD:
        from wsgiref.simple_server import make_server, \
                WSGIServer, WSGIRequestHandler
        WSGIRequestHandler.log_message = lambda *x: None
        httpd = make_server('', 8000, app, server_class=WSGIServer,
                handler_class=WSGIRequestHandler)
        httpd.serve_forever()
    else:
        from flup.server.fcgi import WSGIServer
        WSGIServer(app).run()

