from typing import List

from .ThriftyAttribute import ThriftyAttribute


class IAttributeHolder(object):
    """
    An item that has named attributes attached.
    """
    attributes: List[ThriftyAttribute]
