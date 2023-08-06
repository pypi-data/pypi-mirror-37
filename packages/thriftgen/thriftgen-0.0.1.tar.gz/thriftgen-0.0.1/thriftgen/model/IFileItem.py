class IFileItem(object):
    """
    An item that appears in a thrift file, be it a service,
    struct or exception.
    """
    item_type: str
