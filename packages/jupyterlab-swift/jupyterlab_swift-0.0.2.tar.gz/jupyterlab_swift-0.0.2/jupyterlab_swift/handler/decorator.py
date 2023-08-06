from jupyterlab_swift.handler.exception import FileSizeExceeded, SwiftHandlerException
from keystoneauth1.exceptions import HttpError
from keystoneauth1.exceptions.base import ClientException

def swift_proxy(func):
    """
    A decorator to handle response codes and downstream errors from the
    proxied request. The wrapped function is expected to return a response
    from a `requests` request method.
    """
    def error_response(message):
        return dict(error=message)

    def wrapper(*args, **kwargs):
        context = args[0]

        try:
            func(*args, **kwargs)

        except HttpError as err:
            context.set_status(err.http_status)
            message = err.details if err.details else err.message
            context.finish(error_response(message))

        except FileSizeExceeded as err:
            context.set_status(403) # Forbidden
            context.finish(error_response(err.message))

        except SwiftHandlerException as err:
            context.set_status(400) # Client error
            context.finish(error_response(err.message))

        except ClientException as err:
            context.log.error(err)
            context.set_status(500) # Internal Error
            context.finish(error_response(err.message))

    return wrapper
