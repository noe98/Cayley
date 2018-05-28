"""
File: abstractstack.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection

class AbstractStack(AbstractCollection):
    """Represents an abstract stack."""

    def __init__(self, sourceCollection):
        """Initializes the stack at this level."""
        AbstractCollection.__init__(self, sourceCollection)

    def add(self, item):
        """For compatibility with other collections."""
        self.push(item)
