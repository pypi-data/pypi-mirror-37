from typing import Optional, List

from .ICommentable import ICommentable
from .IFileItem import IFileItem
from .IAttributeHolder import IAttributeHolder

from .ThriftyAttribute import ThriftyAttribute

class ThriftyStruct(ICommentable, IFileItem, IAttributeHolder):
    """
    A struct that can be transported as a type for methods
    or exceptions.
    """

    def __init__(self,
                 name: str,
                 attributes: Optional[List[ThriftyAttribute]] = None) -> None:
        self.name = name
        self.attributes: List[ThriftyAttribute] = attributes or []
        self.comment: Optional[str] = None
        self.item_type = "struct"
