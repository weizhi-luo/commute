"""Represent errors in scraping"""


class StationCrsCodeNotFoundError(KeyError):
    """Represent an error when station crs code is not found"""
    def __init__(self, message: str):
        super().__init__(message)
