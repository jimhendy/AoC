class AoCError(Exception):
    """Base class for AoC errors."""


class PointError(AoCError):
    """Error from the Point Base Class."""


class BinarySearchError(AoCError):
    """Error from the Binary Search Function."""
