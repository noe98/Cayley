"""
Author: Justin Pusztay, Angel Vela
File: linkedstack.py

This file contains the LinkedStack class
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['LinkedStack']

from Cayley.parser.abstractstack import *
from Cayley.parser.node import *

class LinkedStack(AbstractStack):
    """Represents a link-based stack."""

    def __init__(self, sourceCollection = None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._items = None
        AbstractStack.__init__(self, sourceCollection)

    def peek(self):
        """Returns the item at the top of the stack.
        Precondition: the stack is not empty.
        Raises: KeyError if stack is empty."""
        if self.isEmpty():
            raise ValueError("Attempt to peek at empty stack")
        return self._items.data

    def __iter__(self):
        """Supports iteration over a view of self, from bottom to top."""
        def visitNodes(node):
            if not node is None:
                visitNodes(node.next)
                tempList.append(node.data)
        tempList = list()
        visitNodes(self._items)
        return iter(tempList)
        
    # Mutator methods
    
    def clear(self):
        """Makes self become empty."""
        self.resetSizeAndModCount()
        self._items = None        

    def push(self, item):
        """Inserts item at top of the stack."""
        self._items = Node(item, self._items)
        self._size += 1
        self.incModCount()

    def pop(self):
        """Removes and returns the item at the top of the stack.
        Precondition: the stack is not empty.
        Raises: KeyError if stack is empty.
        Postcondition: the top item is removed from the stack."""
        if self.isEmpty():
            raise ValueError("Attempt to pop from empty stack")
        self._size -= 1
        self.incModCount()
        data = self._items.data
        self._items = self._items.next
        return data


def test():
    """Tests a linked stack."""
    stack = LinkedStack(range(5))
    print("Expect [0, 1, 2, 3, 4]: ", stack)
    clone = LinkedStack(stack)
    print("Expect True:", stack == clone)

if __name__ == '__main__': 
    test()
