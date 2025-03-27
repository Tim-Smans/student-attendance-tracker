class NoIdMatchError(Exception):
    """Exception raised for when 2 ids do not match"""

    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message 
        self.error_code = error_code

    def __str__(self):
        return f"API ERROR: {super().__str__()} (Error Code: {self.error_code})"

