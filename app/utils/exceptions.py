class ValidationError(Exception):
    """Exception raised when validation fails"""
    def __init__(self, errors):
        if isinstance(errors, list):
            self.message = "; ".join(errors)
            self.errors = errors
        else:
            self.message = str(errors)
            self.errors = [str(errors)]
        super().__init__(self.message)

class NotFoundException(Exception):
    """Exception raised when a resource is not found"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UnauthorizedException(Exception):
    """Exception khi user không có quyền truy cập"""
    pass 