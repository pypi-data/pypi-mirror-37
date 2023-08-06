import json
from jupyterlab_swift.handler.base import SwiftBaseHandler
from jupyterlab_swift.handler.decorator import swift_proxy
from keystoneauth1.exceptions.http import NotFound
from notebook.utils import url_escape
from notebook.base.handlers import APIHandler
from tornado import gen, web
from tornado.httputil import url_concat

class SwiftMetadataHandler(SwiftBaseHandler, APIHandler):
    """
    A Swift API proxy handler that handles requests for account/container/object
    metadata. Importantly does not handle requests for file contents.
    """

    @web.authenticated
    @gen.coroutine
    @swift_proxy
    def get(self, path=''):
        """
        Proxy API requests to Swift with authenticated session.
        """
        params = self.api_params()
        params['format'] = 'json'
        params['delimiter'] = self.DELIMITER
        api_path = self.api_path(path, params)

        prefix = params.get('prefix')

        if prefix:
            self.log.debug('Proxying to {}'.format(api_path))
            head_response = self.adapter.head(api_path)
            is_directory = self._is_directory_response(head_response)
        else:
            # If no prefix, this is a container listing request.
            is_directory = True
            try:
                head_response = self.adapter.head(api_path)
            except NotFound:
                # Try lazily creating the container once.
                self.adapter.put(api_path)

        if is_directory:
            contents_response = self.adapter.get(api_path)
            self._finish_from_swift_response(contents_response, prefix)
        else:
            self._finish_from_swift_response(head_response)


    def _finish_from_swift_response(self, response, prefix=None):
        """
        Writes a upstream response based on a downstream response from Swift.
        Handles adding minimal type hints for the client about what kinds of
        objects are being returned, as well as making sure to proxy metadata
        headers.
        """
        headers = response.headers

        self.set_status(response.status_code)
        self.set_header('content-type', 'application/json')

        if 'x-account-object-count' in headers:
            # This is an account response
            self.proxy_headers(response, self.ACCOUNT_HEADERS)
            containers = response.json()
            [c.update(type='container') for c in containers]
            self.finish(json.dumps(containers))

        elif 'x-container-object-count' in headers:
            # This is a container response
            self.proxy_headers(response, self.CONTAINER_HEADERS)
            objects = response.json()
            for o in objects:
                if 'subdir' in o:
                    o.update(type='subdir', name=o.pop('subdir'))
                else:
                    o.update(type='object')

                if prefix is not None and self.DELIMITER in prefix:
                    prefix = prefix[0 : prefix.rfind(self.DELIMITER) + 1]
                    o.update(name=o.pop('name').replace(prefix, ''))

            leaf_objects = [o for o in objects if o.get('name')]
            self.finish(json.dumps(leaf_objects))

        else:
            # Assume a file response
            self.proxy_headers(response, self.OBJECT_HEADERS)
            self.finish(json.dumps({
                'hash': headers.get('etag'),
                'last_modified': headers.get('x-timestamp'),
                # For some reason Swift doesn't return _any_ content-length
                # header if the size is 0
                'bytes': int(headers.get('content-length', '0')),
                'content_type': headers.get('content-type'),
                'type': 'object',
            }))

    def _is_directory_response(self, response):
        """
        Determines if a response is for a directory-like entity (account or
        container) based on returned headers.
        """
        headers = response.headers
        return ('x-account-object-count' in headers) or ('x-container-object-count' in headers)
