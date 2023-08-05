# -*- coding: utf-8 -*-
"""
    test_imageembed
    ~~~~~~~~~~~~~~~

    Test sphinxcontrib.imageembed extension.

    :copyright: Copyright 2018 by Jan Gutter <github@jangutter.com>
    :license: BSD, see LICENSE for details.
"""

import pytest


@pytest.mark.sphinx('singlehtml', testroot='sphinxcontrib-imageembed')
def test_sphinxcontrib_imageembed(app, status, warning):
    app.build()

    # content = (app.outdir / 'Python.html').text()
    # assert '\\sphinxincludegraphics{{svgimg}.png}' in content
    # assert not (app.outdir / 'svgimg.svg').exists()
    # assert (app.outdir / 'svgimg.png').exists()
