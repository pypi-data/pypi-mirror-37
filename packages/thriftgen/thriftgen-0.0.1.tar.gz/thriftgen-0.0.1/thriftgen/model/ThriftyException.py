from typing import List, Optional

from .ICommentable import ICommentable
from .IFileItem import IFileItem
from .IAttributeHolder import IAttributeHolder
from .ThriftyAttribute import ThriftyAttribute

class ThriftyException(ICommentable, IFileItem, IAttributeHolder):
    """
    An exception that can be thrown by a service
    """
    name: str
    attributes: List[ThriftyAttribute]

    def __init__(self,
                 name: str,
                 attributes: Optional[List[ThriftyAttribute]] = None) -> None:
        self.name = name
        self.attributes = attributes or []
        self.comment = None
        self.item_type = "exception"
