from typing import Optional


class ICommentable(object):
    """
    An item that might have a comment attached to it.
    """
    comment: Optional[str]
