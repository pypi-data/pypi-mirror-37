from .__meta__ import __version__

from .widget_upload import FileUpload
# from .widget_upload_box import FileUploadBox


def _jupyter_nbextension_paths():
    return [{
        # fixed syntax
        'section': 'notebook',
        # path relative to module directory - here: ipyupload
        'src': 'static',
        # directory in the `nbextension/` namespace
        'dest': 'ipyupload',
        # path in the `nbextension/` namespace
        'require': 'ipyupload/extension'
    }]
