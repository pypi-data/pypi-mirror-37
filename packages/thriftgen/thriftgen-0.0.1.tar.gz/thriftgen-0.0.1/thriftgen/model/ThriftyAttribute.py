from .ICommentable import ICommentable
from .ThriftyType import ThriftyType

class ThriftyAttribute(ICommentable):
    """
    An attribute that can belong to a method, a struct, or
    an exception.
    """
    name: str
    attrtype: ThriftyType

    def __init__(self,
                 name: str,
                 attrtype: ThriftyType) -> None:
        self.name = name
        self.attrtype = attrtype
        self.comment = None