from os import environ
from traitlets import Unicode
from traitlets.config import Configurable

class SwiftConfig(Configurable):
    """
    Allows configuration of access to the Swift API
    """
    auth_url = Unicode(
        environ.get('OS_AUTH_URL', ''), config=True,
        help=""
    )
    token = Unicode(
        environ.get('OS_TOKEN', ''), config=True,
        help=("")
    )
    project_name = Unicode(
        environ.get('OS_PROJECT_NAME', ''), config=True,
        help=""
    )
    project_domain_name = Unicode(
        environ.get('OS_PROJECT_DOMAIN_NAME', ''), config=True,
        help=""
    )
    interface = Unicode(
        environ.get('OS_INTERFACE', 'public'), config=True,
        help=""
    )
    region_name = Unicode(
        environ.get('OS_REGION_NAME', ''), config=True,
        help=""
    )
