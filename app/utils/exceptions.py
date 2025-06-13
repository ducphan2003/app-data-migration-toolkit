class ValidationError(Exception):
    """Exception khi validate dữ liệu thất bại"""
    pass

class NotFoundException(Exception):
    """Exception khi không tìm thấy resource"""
    pass

class UnauthorizedException(Exception):
    """Exception khi user không có quyền truy cập"""
    pass 