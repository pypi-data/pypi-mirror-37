"""
Drift Deck

Usage:
  driftdeck <slides.md> [--css <custom.css>]
  driftdeck (-h | --help)
  driftdeck --version

Options:
  --css <custom.css>    Provide your custom css for markdown
  -h --help             Show this screen.
  --version             Show version.
"""

import os
import webbrowser
from io import open
from string import Template
from pkg_resources import resource_string, get_distribution

from docopt import docopt
from markdown import markdown

from driftdeck.httpd import ThreadedHTTPServer


def convert(title: str, md: str, slide: int, total: int) -> str:
    """

    :param md: the markdown of one slide
    :param slide: number of the slide
    :param total: total number of slides
    :return:
    """
    html = markdown(md, extensions=['markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.nl2br',
                                     'markdown.extensions.sane_lists',
                                     'markdown.extensions.smarty'])

    numbers = ''.join(['<span%s>%d</span>' % (' class="active"' if i == slide else '', i) for i in range(1, total + 1)])

    return Template(resource_string(__name__, 'slide.html').decode()) \
        .safe_substitute(dict(title=title, content=html, numbers=numbers, total=total,
                              a_prev='<a href="/%d">&lt;</a>' % (slide - 1) if slide > 1 else '',
                              a_next='<a href="/%d">&gt;</a>' % (slide + 1) if slide < total else '',
                              prev=slide - 1 if slide > 1 else 1,
                              next=slide + 1 if slide < total else total))


def start():
    args = docopt(__doc__, version='Drift Deck v%s' % get_distribution('driftdeck').version)

    if args['--css'] and os.path.isfile(args['--css']):
        with open(args['--css'], 'r') as fd:
            custom_css = fd.read()
    else:
        custom_css = None

    markupfile = os.path.expanduser(args['<slides.md>'])
    title = os.path.basename(markupfile)
    with open(markupfile, 'r') as fd:
        mdslides = fd.read().split('---\n')

    htmlslides = []
    for i, slide in enumerate(mdslides, start=1):
        htmlslides.append(convert(title, slide, int(i), len(mdslides)))
    del mdslides

    with ThreadedHTTPServer(slides=htmlslides, css=custom_css) as s:
        webbrowser.open('http://localhost:%d/1' % s.server.server_port)
        input('Running presentation, press <Enter> to quit...')
