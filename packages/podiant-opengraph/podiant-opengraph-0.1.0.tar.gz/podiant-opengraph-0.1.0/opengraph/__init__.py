from bs4 import BeautifulSoup
import json
import re
import requests


__version__ = '0.1.0'
__all__ = ['OpenGraph']


class OpenGraph(dict):
    required_attrs = [
        'title',
        'type',
        'image',
        'url',
        'description'
    ]

    def __init__(self, url=None, html=None, scrape=False, **kwargs):
        # If scrape is True, then try to fetch missing attribtues from the
        # page's body

        self.scrape = scrape
        self._url = url

        for key in kwargs.keys():
            self[key] = kwargs[key]

        dict.__init__(self)

        if url is not None:
            self.fetch(url)

        if html is not None:
            self.parser(html)

    def __setattr__(self, name, val):
        self[name] = val

    def __getattr__(self, name):
        return self[name]

    def fetch(self, url):
        response = requests.get(url)
        return self.parser(response.content)

    def parser(self, html):
        doc = html
        if not isinstance(html, BeautifulSoup):
            doc = BeautifulSoup(html, 'html.parser')

        ogs = doc.html.head.findAll(
            property=re.compile(r'^og')
        )

        for og in ogs:
            if og.has_attr('content'):
                self[og['property'][3:]] = og['content']

        if not self.is_valid() and self.scrape:
            # Couldn't fetch all attrs from og tags; try scraping body
            for attr in self.required_attrs:
                if not self.valid_attr(attr):
                    try:
                        self[attr] = getattr(self, 'scrape_%s' % attr)(doc)
                    except AttributeError:  # pragma: no cover
                        pass

    def valid_attr(self, attr):
        return self.get(attr) and len(self[attr]) > 0

    def is_valid(self):
        return all(
            [
                self.valid_attr(attr)
                for attr in self.required_attrs
            ]
        )

    def to_html(self):
        if not self.is_valid():
            return (
                '<meta property="og:error" '
                'content="og metadata is not valid" />'
            )

        meta = ''
        for key, value in self.items():
            meta += '\n<meta property="og:%s" content="%s" />' % (
                key,
                value
            )

        meta += '\n'
        return meta

    def to_json(self):
        if not self.is_valid():
            return json.dumps(
                {
                    'error': 'og metadata is not valid'
                }
            )

        return json.dumps(self)

    def scrape_image(self, doc):
        images = [
            dict(img.attrs).get('src')
            for img in doc.html.body.findAll('img')
        ]

        for image in images:
            if image:
                return image

        return ''  # pragma: no cover

    def scrape_type(self, doc):
        return 'other'

    def scrape_title(self, doc):
        return doc.html.head.title.text

    def scrape_url(self, doc):
        return self._url

    def scrape_description(self, doc):
        tag = doc.html.head.findAll(
            'meta',
            attrs={
                'name': 'description'
            }
        )

        result = ''.join(
            [
                t['content']
                for t in tag
            ]
        )

        return result
