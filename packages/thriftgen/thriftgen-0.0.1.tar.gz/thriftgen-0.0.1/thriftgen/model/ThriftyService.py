from typing import List, Optional

from .ICommentable import ICommentable
from .IFileItem import IFileItem

from .ThriftyMethod import ThriftyMethod

class ThriftyService(ICommentable, IFileItem):
    """
    ThriftyService is a service that exports one or more methods.
    """
    name: str

    def __init__(self,
                 name: str,
                 methods: Optional[List[ThriftyMethod]] = None) -> None:
        self.name = name
        self.methods: List[ThriftyMethod] = methods or []
        self.comment = None
        self.item_type = "service"
