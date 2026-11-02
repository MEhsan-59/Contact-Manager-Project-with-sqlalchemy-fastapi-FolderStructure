class AppException(Exception):
    def __init__(self, message: str | None = None, error_code : str = "Bad Request", status_code: int = 400):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)
    
class ContactNotFoundException(AppException):
    def __init__(self, message: str = "Contact not found."):
        super().__init__(message=message, status_code=404, error_code="CONTACT_NOT_FOUND")


class DuplicateException(AppException):
    def __init__(self, message: str = "Contact already exists in the group."):
        super().__init__(message=message, status_code=400, error_code="DUPLICATE_GROUP_CONTACT")
