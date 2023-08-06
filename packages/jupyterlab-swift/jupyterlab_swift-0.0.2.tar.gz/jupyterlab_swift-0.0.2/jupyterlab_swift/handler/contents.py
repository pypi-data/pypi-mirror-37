from jupyterlab_swift.handler.base import SwiftBaseHandler
from jupyterlab_swift.handler.decorator import swift_proxy
from jupyterlab_swift.handler.exception import SwiftHandlerException, FileSizeExceeded
from keystoneauth1.exceptions import HttpError
from keystoneauth1.exceptions.base import ClientException
from notebook.utils import url_escape
from notebook.base.handlers import AuthenticatedFileHandler
from tornado import gen, web
from tornado.httputil import url_concat

class SwiftContentsHandler(SwiftBaseHandler, AuthenticatedFileHandler):
    """
    A Swift API proxy handler that handles requests for account/container/object
    metadata. Importantly does not handle requests for file contents.
    """

    COPY_HEADER = 'x-copy-from'

    @web.authenticated
    @gen.coroutine
    @swift_proxy
    def get(self, path=''):
        """
        Proxy GET API requests to Swift with authenticated session.
        """
        self._check_path(path)

        api_path = self.api_path(path, self.api_params())

        head_response = self.adapter.head(api_path)
        self._check_content_length(head_response.headers)

        response = self.adapter.get(api_path)

        self.set_status(response.status_code)
        self.proxy_headers(response, self.OBJECT_HEADERS)
        self.proxy_headers(response, ['content-length', 'content-type'])
        self.finish(response.content)

    @web.authenticated
    @gen.coroutine
    @swift_proxy
    def put(self, path=''):
        """
        Proxy PUT API requests to Swift with authenticated session.
        """
        request_headers = self.request.headers
        self._check_path(path)
        self._check_content_length(request_headers)

        proxied_headers = {}
        if self.COPY_HEADER in request_headers:
            copy_from = self.swift_path(request_headers.get(self.COPY_HEADER))
            proxied_headers[self.COPY_HEADER] = copy_from

        response = self.adapter.put(self.api_path(path, self.api_params()),
                                    headers=proxied_headers,
                                    data=self.request.body)

        self.set_status(response.status_code)
        self.proxy_headers(response, self.OBJECT_HEADERS)
        self.proxy_headers(response, ['content-length', 'content-type'])
        self.finish()

    @web.authenticated
    @gen.coroutine
    @swift_proxy
    def delete(self, path=''):
        """
        Proxy DELETE API requests to Swift with authenticated session.
        """
        self._check_path(path)

        response = self.adapter.delete(self.api_path(path, self.api_params()))
        self.set_status(response.status_code)
        self.finish()

    def _check_path(self, path):
        """
        Ensure there is a path set on the request. Avoids problems where
        requests are made implicitly against the container itself rather
        than an object in a container (especially important for DELETE)
        """
        if not path.replace('/', ''):
            raise SwiftHandlerException('No path to file')

    def _check_content_length(self, headers):
        """
        Ensure the file does not exceed some maximum size. All file downloads
        and uploads are proxied through this handler, which causes strain, and the
        Jupyter interface doesn't deal well with huge files anyways.
        """
        # For some reason Swift doesn't return _any_ content-length
        # header if the size is 0
        file_size = int(headers.get('content-length', '0'))
        max_size = self.swift_config.max_file_size_bytes
        if file_size > max_size:
            raise FileSizeExceeded('File exceeds max size of {} bytes'.format(max_size))
