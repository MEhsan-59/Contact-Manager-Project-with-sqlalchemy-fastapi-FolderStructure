class ContactError(Exception):
    status_code = 400
    message = "Bad request."

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(self.message)


class ContactNotFoundException(ContactError):
    status_code = 404
    message = "Contact not found."