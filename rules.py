import re

wt.add_rule(re.compile('^%s/(.*)$' % STATIC_URL), static_serve,
                ['static_file'])

wt.add_rule(re.compile('^%s/blog/([a-za-z0-9\-]+)$' % BASE_URL), blog_page,
                ['entry'])

wt.add_rule(re.compile('^%s/page/([a-za-z0-9\-]+)$' % BASE_URL), page_page,
                ['entry'])

wt.add_rule(re.compile('^%s/category/(.+)$' % BASE_URL),
                category_page, ['category'])

# This should be the last rule.
wt.add_rule(re.compile('^%s/?$' % BASE_URL), main_page, [])
