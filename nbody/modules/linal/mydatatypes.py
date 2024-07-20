from typing import Iterable


class TubeList:
    """List with fixed lenght, where you can read any element,\n
    but adding just on top like in stack,\n
    If the tubelist is full, adding new values will pop the bottom element\n
    When tubelist is created, the lenght is checked, gives error when you trying to init it with more element\n
    """
    def __init__(self, values: Iterable, depth: int):
        self.values = values
        self.depth = depth

class Node:
    """Node for stack
    """
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    """Classic stack
    """
    def __init__(self):
        self.head = Node("head")
        self.size = 0

    def __str__(self):
        cur = self.head.next
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]

    def len(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def peek(self):

        if self.isEmpty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value

    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1

    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value
