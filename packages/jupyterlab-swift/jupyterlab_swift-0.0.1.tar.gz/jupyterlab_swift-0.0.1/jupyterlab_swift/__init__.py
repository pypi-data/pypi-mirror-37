from jupyterlab_swift.config import SwiftConfig
from jupyterlab_swift.handler import SwiftContentsHandler, SwiftMetadataHandler
from notebook.utils import url_path_join

import logging
logging.basicConfig()

__version__ = '0.0.1'

def _jupyter_server_extension_paths():
    return [{
        'module': 'jupyterlab_swift'
    }]

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    base_url = web_app.settings['base_url']

    base_endpoint = url_path_join(base_url, 'swift')
    contents_endpoint = url_path_join(base_endpoint, 'contents')
    meta_endpoint = url_path_join(base_endpoint, 'meta')
    handlers = [(contents_endpoint + "(.*)", SwiftContentsHandler),
                (meta_endpoint + "(.*)", SwiftMetadataHandler)]

    host_pattern = '.*$'
    web_app.add_handlers(host_pattern, handlers)
