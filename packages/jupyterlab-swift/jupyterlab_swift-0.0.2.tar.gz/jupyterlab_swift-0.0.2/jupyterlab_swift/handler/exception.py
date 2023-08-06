class SwiftHandlerException(Exception):
   """
   Base class for other exceptions
   """
   def __init__(self, message='An unexpected error occurred'):
       self.message = message

class FileSizeExceeded(SwiftHandlerException):
   """
   Raised when an uploaded or downloaded file exceeds the maximum threshold
   """
   pass
