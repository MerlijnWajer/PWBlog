import re

wt.add_rule(re.compile('^%s/(.*)$' % STATIC_URL), static_serve,
                ['static_file'])

wt.add_rule(re.compile('^%s/blog/([A-Za-z0-9]+)$' % BASE_URL), blog_page,
                ['filename'])

# This should be the last rule.
wt.add_rule(re.compile('^%s/?$' % BASE_URL), main_page, [])
