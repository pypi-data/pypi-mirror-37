from jupyterlab_swift.config import SwiftConfig
from keystoneauth1.adapter import Adapter
from keystoneauth1.identity import v3
from keystoneauth1.session import Session
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_escape
from re import sub
from tornado.httputil import url_concat

class SwiftBaseHandler(IPythonHandler):
    DELIMITER = '/'

    ACCOUNT_HEADERS = (
        'x-account-access-control',
        'x-account-bytes-used',
        'x-account-container-count',
        'x-account-meta-name',
        'x-account-meta-quota-bytes',
        'x-account-meta-temp-url-key-2',
        'x-account-meta-temp-url-key',
        'x-account-object-count',
        'x-account-storage-policy-name-bytes-used',
        'x-account-storage-policy-name-container-count',
        'x-account-storage-policy-name-object-count',
        'x-openstack-request-id',
        'x-timestamp',
    )

    CONTAINER_HEADERS = (
        'x-container-bytes-used',
        'x-container-meta-name',
        'x-container-meta-quota-bytes',
        'x-container-meta-quota-count',
        'x-container-meta-temp-url-key-2',
        'x-container-meta-temp-url-key',
        'x-container-object-count',
        'x-container-read',
        'x-container-sync-key',
        'x-container-sync-to',
        'x-container-write',
        'x-history-location',
        'x-openstack-request-id',
        'x-storage-policy',
        'x-timestamp',
        'x-versions-location',
    )

    OBJECT_HEADERS = (
        'x-delete-at',
        'x-object-manifest',
        'x-object-meta-name',
        'x-openstack-request-id',
        'x-static-large-object',
        'x-symlink-target-account',
        'x-symlink-target',
        'x-timestamp',
    )

    """
    A base clase for a Swift API proxy handler.
    """
    def initialize(self):
        conf = self.swift_config = SwiftConfig(config=self.config)
        auth = v3.Token(auth_url=conf.auth_url,
                        token=conf.token,
                        project_name=conf.project_name,
                        project_domain_name=conf.project_domain_name)
        session = Session(auth=auth)
        self.adapter = Adapter(session=session,
                               service_type='object-store',
                               interface=conf.interface,
                               region_name=conf.region_name)

    def proxy_headers(self, response, names):
        headers = response.headers
        [self.set_header(x, headers.get(x)) for x in names if x in headers]

    def swift_path(self, path):
        container = self.root_container()
        path_parts = list(filter(None, [container, sub('^/', '', path)]))
        return self.DELIMITER.join(path_parts)

    def api_path(self, path, params=None):
        return url_concat(url_escape(self.swift_path(path)), params)

    def api_params(self):
        query = self.request.query_arguments
        return { key: query[key][0].decode() for key in query }

    def root_container(self):
        conf = self.swift_config
        if not conf.root_container:
            return None
        return conf.root_container.format(project_name=conf.project_name)

    def _is_directory_response(self, response):
        """
        Determines if a response is for a directory-like entity (account or
        container) based on returned headers.
        """
        headers = response.headers
        return ('x-account-object-count' in headers) or ('x-container-object-count' in headers)
