from typing import List

from .IFileItem import IFileItem

class ThriftyFile(object):
    """
    A file that contains multiple services, structures and exceptions.
    """
    file_name: str
    file_items: List[IFileItem]

    def __init__(self,
                 file_name: str) -> None:
        self.file_name = file_name
        self.file_items = []
