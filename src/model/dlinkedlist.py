# src/model/doubly_linked_list.py

class DNode:
    def __init__(self, value, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev

    def __str__(self):
        return str(self.value)


class DLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def insert_back(self, value):
        new_node = DNode(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert_front(self, value):
        new_node = DNode(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def delete_back(self):
        if self.is_empty():
            raise IndexError("Cannot delete from empty list")
        removed = self.tail
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = removed.prev
            self.tail.next = None
        self.size -= 1
        return removed.value

    def delete_front(self):
        if self.is_empty():
            raise IndexError("Cannot delete from empty list")
        removed = self.head
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = removed.next
            self.head.prev = None
        self.size -= 1
        return removed.value

    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __str__(self):
        values = [str(node) for node in self]
        return " <-> ".join(values) + " <-> None" if values else "Empty list"
