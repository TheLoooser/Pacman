"""
This module contains an implementation of a node.
Source code: https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
"""

from __future__ import annotations


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent: Node = None, position: tuple[int, int] = None) -> None:
        """
        Constructs a node object.

        :param parent: The parent node.
        :param position: The position of the node.
        """
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: Node) -> bool:
        """
        Defines equal comparator between nodes.

        :param other: Another node.
        :return: True if the node equal to the other node, False otherwise.
        """
        return self.position == other.position

    def __repr__(self) -> str:
        """
        Creates a string representation of the node.

        :return: The string representation.
        """
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    #
    def __lt__(self, other: Node) -> bool:
        """
        Defining less than for purposes of heap queue

        :param other: Another node.
        :return: True if the node is smaller than the other node, False otherwise.
        """
        return self.f < other.f

    def __gt__(self, other: Node) -> bool:
        """
        Defining greater than for purposes of heap queue

        :param other: Another node.
        :return: True if the node is greater than the other node, False otherwise.
        """
        return self.f > other.f
