"""
File: node.py
Author: Justin Pusztay
"""

__author__ = "\n".join(['Justin Pusztay (pusztayj20@mail.wlu.edu)'])

__all__ = ['Node']

class Node(object):
    """Nodes for singly linked structures."""

    def __init__(self, data, next = None):
        """Instantiates a Node with default next of None"""
        self.data = data
        self.next = next
