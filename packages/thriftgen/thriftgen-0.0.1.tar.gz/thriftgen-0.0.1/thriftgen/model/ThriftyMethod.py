from typing import List, Optional

from .ICommentable import ICommentable
from .IAttributeHolder import IAttributeHolder

from .ThriftyAttribute import ThriftyAttribute
from .ThriftyType import ThriftyType


class ThriftyMethod(ICommentable, IAttributeHolder):
    """
    Just a basic service method
    """
    def __init__(self,
                 name: str,
                 attributes: Optional[List[ThriftyAttribute]] = None,
                 exceptions: Optional[List[ThriftyAttribute]] = None,
                 return_type: Optional[ThriftyType] = None) -> None:
        self.name = name
        self.attributes = attributes or []
        self.exceptions = exceptions or []
        self.comment = None
        self.return_type: ThriftyType = return_type or ThriftyType("void")
