from os import environ
from traitlets import Integer, Unicode
from traitlets.config import Configurable

class SwiftConfig(Configurable):
    """
    Allows configuration of access to the Swift API
    """
    auth_url = Unicode(
        environ.get('OS_AUTH_URL', ''), config=True,
        help="OpenStack Keystone URL"
    )
    token = Unicode(
        environ.get('OS_TOKEN', ''), config=True,
        help="OpenStack Keystone token"
    )
    project_name = Unicode(
        environ.get('OS_PROJECT_NAME', ''), config=True,
        help="OpenStack Keystone project name (Keystone v3)"
    )
    project_domain_name = Unicode(
        environ.get('OS_PROJECT_DOMAIN_NAME', ''), config=True,
        help="OpenStack Keystone project domain name (Keystone v3)"
    )
    interface = Unicode(
        environ.get('OS_INTERFACE', 'public'), config=True,
        help="OpenStack endpoint interface type"
    )
    region_name = Unicode(
        environ.get('OS_REGION_NAME', ''), config=True,
        help="OpenStack region name"
    )
    root_container = Unicode(
        "jupyter:{project_name}", config=True,
        help=("A root Swift container to mount - if not defined, all containers "
              "are mounted under a dummy directory")
    )
    max_file_size_bytes = Integer(
        1024*1024, config=True,
        help="Maximum file size (in bytes) to allow when uploading or downloading"
    )
