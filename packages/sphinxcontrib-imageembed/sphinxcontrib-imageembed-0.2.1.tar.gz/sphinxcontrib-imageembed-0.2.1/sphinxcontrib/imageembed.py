"""
    sphinxcontrib.imageembed
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Embed images directly into generated html docs.

    :copyright: Copyright 2018 by Jan Gutter <github@jangutter.com>
    :license: BSD, see LICENSE for details.
"""

import base64
import os

from six import text_type
from sphinx.transforms.post_transforms.images import ImageConverter
from sphinx.util import logging
from sphinx.util.images import guess_mimetype

try:
    import pbr.version
    __version__ = pbr.version.VersionInfo('imageembed').version_string()
except ImportError:
    __version__ = '0.0.0'

if False:
    # For type annotations
    from docutils import nodes  # noqa
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

logger = logging.getLogger(__name__)


def _convert_to_data_uri(filename):
    # type: (str) -> str
    encoded = base64.b64encode(open(filename, "rb").read())
    mimetype = guess_mimetype(filename, default='*')
    data_uri = 'data:{};base64,{}'.format(mimetype, encoded)
    return data_uri


class ImageEmbedder(ImageConverter):
    default_priority = 200

    def match(self, node):
        # type: (nodes.Node) -> bool
        if self.app.builder.supported_image_types == []:
            return False
        else:
            return self.app.builder.supported_data_uri_images

    def handle(self, node):
        # type: (nodes.Node) -> None
        try:
            node['alt'] = node['uri']
            basename = os.path.basename(node['uri'])
            path = os.path.join(self.app.srcdir, basename)
            node['uri'] = _convert_to_data_uri(path)
        except Exception as exc:
            logger.error('Could not embed image: %s [%s]' % (node['alt'],
                                                             text_type(exc)))


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    app.add_post_transform(ImageEmbedder)
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
