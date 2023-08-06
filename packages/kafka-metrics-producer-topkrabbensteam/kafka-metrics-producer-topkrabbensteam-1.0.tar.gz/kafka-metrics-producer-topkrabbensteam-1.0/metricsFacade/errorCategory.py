from enum import Enum
class ErrorCategory(Enum):
    ServerError = 1
    ValidationError = 2
    ProxyError = 3,
    NotFound = 4,
    BanError = 5
