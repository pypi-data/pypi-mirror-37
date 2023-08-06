class ThriftyType(object):
    """
    A type that can be used in a method parameter, struct, or exception
    member definition.
    """
    def __init__(self, name: str) -> None:
        self.name: str = name
