
import random
import ipywidgets as wg

from traitlets import observe, validate, Unicode, Dict, List, Int, Bool, Bytes, TraitError

from .util import Util
from .__meta__ import __version_js__

_semver_range_frontend_ = '~' + __version_js__


class FileUpload(wg.DOMWidget):
    """
    File upload widget
    """
    _model_name = Unicode('FileUploadModel').tag(sync=True)
    _view_name = Unicode('FileUploadView').tag(sync=True)
    _model_module = Unicode('ipyupload').tag(sync=True)
    _view_module = Unicode('ipyupload').tag(sync=True)
    _view_module_version = Unicode(_semver_range_frontend_).tag(sync=True)
    _model_module_version = Unicode(_semver_range_frontend_).tag(sync=True)

    _id = Int(0).tag(sync=True)
    _counter = Int(0).tag(sync=True)

    help = 'Type of files the input accepts. None for all. See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#attr-accept'
    accept = Unicode(help=help).tag(sync=True)

    help = 'If true, allow for multiple files upload, else only accept one'
    multiple = Bool(False, help=help).tag(sync=True)

    help = 'Enable or disable button.'
    disabled = Bool(False, help=help).tag(sync=True)

    help = 'Optional style for button (label element)'
    style_button = Unicode('', help=help).tag(sync=True)

    help = 'Compress level: from 1 to 9 - 0 for no compression'
    compress_level = Int(0, help=help).tag(sync=True)

    help = 'List of file metadata'
    li_metadata = List(Dict, help=help).tag(sync=True)

    help = 'List of file content (bytes)'
    li_content = List(Bytes, help=help).tag(sync=True,
                                            from_json=Util.content_from_json)

    help = 'Error message'
    error = Unicode('', help=help).tag(sync=True)

    value = Dict({}).tag(sync=False)

    def __init__(self,
                 accept='',
                 multiple=False,
                 disabled=False,
                 style_button='',
                 compress_level=0,
                 ):
        """
        Instantiate widget
        """

        if accept is None:
            accept = ''

        if style_button is None:
            style_button = ''

        self._id = random.randint(0, int(1e9))
        self._counter = 0

        self.accept = accept
        self.disabled = disabled
        self.multiple = multiple
        self.style_button = style_button
        self.compress_level = compress_level

        self.value = {}

        super().__init__()

    @validate('compress_level')
    def _valid_compress_level(self, proposal):
        if proposal['value'] not in range(10):
            raise TraitError('compress_level must be an int from 0 to 9 incl.')
        return proposal['value']

    @observe('_counter')
    def on_incr_counter(self, change):
        """
        """
        res = {}

        msg = 'Error: length of li_metadata and li_content must be equal'
        assert len(self.li_metadata) == len(self.li_content), msg

        for metadata, content in zip(self.li_metadata,
                                     self.li_content):
            name = metadata['name']
            res[name] = {'metadata': metadata, 'content': content}

        self.value = res
