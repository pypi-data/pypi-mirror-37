from typing import Optional, List

from .ICommentable import ICommentable
from .IFileItem import IFileItem

class ThriftyEnum(ICommentable, IFileItem):
    """
    An enum that's defined in the thrift file.
    """
    name: str
    values: List[str]

    def __init__(self,
                 name: str,
                 values: Optional[List[str]] = None) -> None:
        self.name: str = name
        self.values: List[str] = values or []
        self.comment: Optional[str] = None
        self.item_type: str = "enum"
