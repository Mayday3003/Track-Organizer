class DNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        return str(self.value)

class CDLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self) -> bool:
        return self.size == 0

    def insert_back(self, value):
        new_node = DNode(value)
        if self.is_empty():
            self.head = self.tail = new_node
            new_node.next = new_node.prev = new_node
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node
        self.size += 1

    def insert_front(self, value):
        new_node = DNode(value)
        if self.is_empty():
            self.head = self.tail = new_node
            new_node.next = new_node.prev = new_node
        else:
            new_node.next = self.head
            new_node.prev = self.tail
            self.head.prev = new_node
            self.tail.next = new_node
            self.head = new_node
        self.size += 1

    def delete_node(self, node: DNode):
        if self.is_empty() or node is None:
            return None
        if self.size == 1 and node == self.head:
            val = node.value
            self.head = self.tail = None
            self.size = 0
            return val
        # unlink node
        node.prev.next = node.next
        node.next.prev = node.prev
        val = node.value
        if node == self.head:
            self.head = node.next
        if node == self.tail:
            self.tail = node.prev
        self.size -= 1
        return val

    def delete_front(self):
        return self.delete_node(self.head)

    def delete_back(self):
        return self.delete_node(self.tail)

    def __len__(self) -> int:
        return self.size

    def __iter__(self):
        if self.is_empty():
            return
        current = self.head
        for _ in range(self.size):
            yield current.value
            current = current.next

    def __str__(self) -> str:
        if self.is_empty():
            return "Empty list"
        values = []
        current = self.head
        for _ in range(self.size):
            values.append(str(current.value))
            current = current.next
        return " <-> ".join(values)
