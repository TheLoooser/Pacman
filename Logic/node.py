"""
Source code: https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
"""

from __future__ import annotations


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent: Node = None, position: tuple[int, int] = None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: Node) -> bool:
        return self.position == other.position

    def __repr__(self) -> str:
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other: Node) -> bool:
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other: Node) -> bool:
        return self.f > other.f
