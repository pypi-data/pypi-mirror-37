# Jupyter custom ipywidget: **ipyupload**

[![Latest Version](https://img.shields.io/pypi/v/ipyupload.svg)](https://pypi.python.org/pypi/ipyupload/)
[![Downloads](https://img.shields.io/pypi/dm/ipyupload.svg)](https://pypi.python.org/pypi/ipyupload/)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gl/oscar6echo%2Fipyupload-repo2docker/master?filepath=demo-ipyupload.ipynb)

## 1 - Overview

This repo contains the source code and the building scripts for **ipyupload** a custom [ipywidget](https://ipywidgets.readthedocs.io/en/stable/).

It enables to upload a file from a Jupyter notebook - classic or JupyterLab.

<div style="display:block; margin: 0 auto; text-align:center">
<img src="img/demo-ipyupload.gif" width="700">
</div>

It allows:

-   single or multiple file upload
-   to restrict the upload to certain file types
-   to disable the file upload

Under the hood:

-   The [FileReader](https://developer.mozilla.org/en-US/docs/Web/API/FileReader) Web API is used.
-   Data is read throught the [readAsArrayBuffer()](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsArrayBuffer) method, then converted to a [DataView](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) before syncing back to Python.
-   The convertion to Python bytes uses the ipywidgets deserializer [bytes_serialization](https://github.com/jupyter-widgets/ipywidgets/blob/a5709728f71e21c81a89e8d123dde2068dd1e74d/ipywidgets/widgets/trait_types.py#L196) already used for the [Media core widget](https://github.com/jupyter-widgets/ipywidgets/blob/a5709728f71e21c81a89e8d123dde2068dd1e74d/ipywidgets/widgets/widget_media.py#L36).
-   The metadata are synced back as a `List(Dict)`.
-   The file contents are synced back as a `List(Bytes)`.
-   An `Int` counter is observed and upon change triggers the aggregation of the data and presentation to the user as a dict {filename: {metadata, file content in bytes}) in the `.value` property.
-   Data can be compressed (optionally) from the browser (using [pako.deflate](https://nodeca.github.io/pako/#deflate)) to the Python kernel (using [zlib.decompress](https://docs.python.org/3/library/zlib.html)). 

After an upload the button displays the number of files uploaded, to provide feedback to the user.

Naturally such an upload widget is mostly useful in a widgetized notebook and/or in a JupyterHub context, with a remote kernel.

## 2 - Install

## 2.1 - User Install

From terminal:

```bash
# for notebook >= 5.3
$ pip install ipyupload

# for notebook < 5.3
$ pip install ipyupload
$ jupyter nbextension install ipyupload --py --sys-prefix
```

## 2.2 - Developer Install

From terminal:

```bash
$ git clone https://gitlab.com/oscar6echo/ipyupload.git
$ cd ipyupload/js
$ npm install
$ cd ..
$ pip install -e .
$ jupyter nbextension install --py --symlink --sys-prefix ipyupload
$ jupyter nbextension enable --py --sys-prefix ipyupload
```

# 3 - Use

```python
from IPython.display import display
from ipyupload import FileUpload

w = FileUpload(
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#attr-accept
    # eg. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
    accept='', # default
    # True to accept multiple files upload else False
    multiple=False, # default
    # True to disable the button else False to enable it
    disabled=False, # default
    # CSS transparently passed to button (a button element overlays the input[type=file] element for better styling)
    # e.g. 'color: darkblue; background-color: lightsalmon; width: 180px;'
    style_button='' # default
    # to compress data from browser to kernel
    # compress level from 1 to 9 incl. - 0 for no compression
    compress_level=0 # default
)
display(w)
```

For more examples:

-   See the [demo notebook](https://nbviewer.jupyter.org/urls/gitlab.com/oscar6echo/ipyupload/raw/master/notebooks/demo-ipyupload.ipynb) on [nbviewer](https://nbviewer.jupyter.org/).
-   Run it on [mybinder.org](https://mybinder.org/): [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gl/oscar6echo%2Fipyupload-repo2docker/master?filepath=demo-ipyupload.ipynb)
