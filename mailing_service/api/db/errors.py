class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""
    pass


class PhoneLengthError(Exception):
    """Raised when phone length is not equal to 7 digits."""
    pass


class TimezoneError(Exception):
    """Raised when input timezone is not in the list of timezones."""
    pass


class UserCredentialsError(Exception):
    """Raised when username or password are incorrect."""
    pass
