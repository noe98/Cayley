"""
File: abstractstack.py
Author: Justin Pusztay
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['AbstractStack']

from Cayley.parser.abstractcollection import *

class AbstractStack(AbstractCollection):
    """Represents an abstract stack."""

    def __init__(self, sourceCollection):
        """Initializes the stack at this level."""
        AbstractCollection.__init__(self, sourceCollection)

    def add(self, item):
        """For compatibility with other collections."""
        self.push(item)
