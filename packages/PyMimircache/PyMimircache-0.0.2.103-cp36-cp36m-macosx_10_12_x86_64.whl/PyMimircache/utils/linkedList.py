# coding=utf-8

"""
    A implementation of linkedlist


"""


class LinkedListNode:
    def __init__(self):
        self.content = None
        self.id = -1
        self.next = None
        self.prev = None

    def set_id(self, id):
        self.id = id


class LinkedList:
    def __init__(self):
        """
        initialization of the linkedlist, head does not contain any element, but head contains last element
        :return:
        """
        self.head = LinkedListNode()
        self.tail = None
        self.size = 0
        self.currentNode = self.head
        # self.max_size = maxlen

    def insert_at_tail(self, content, **kargs):
        node = LinkedListNode()
        node.content = content
        if 'id' in kargs:
            node.id = kargs['id']
        node.next = None
        if self.tail:
            # the list is not empty
            node.prev = self.tail
            self.tail.next = node
        else:
            self.head.next = node
            node.prev = self.head
        self.tail = node
        self.size += 1

        # if self.max_size!=-1 and self.size>self.max_size:
        #     self.remove_from_tail()

        return node

    def insert_node_at_tail(self, node):
        node.next = None
        if self.tail:
            # the list is not empty
            node.prev = self.tail
            self.tail.next = node
        else:
            self.head.next = node
            node.prev = self.head
        self.tail = node
        self.size += 1

        return node

    def insert_at_head(self, content, **kargs):
        node = LinkedListNode()
        node.content = content
        if 'id' in kargs:
            node.id = kargs['id']
        node.next = self.head.next
        if self.head.next:
            self.head.next.prev = node
        else:
            self.tail = node
        self.head.next = node
        node.prev = self.head
        self.size += 1
        return node

    def remove_from_tail(self):
        tail = self.tail
        self.tail.prev.next = None
        temp = self.tail.prev
        self.tail.prev = None
        self.tail = temp
        self.size -= 1
        return tail.content

    def remove_from_head(self):
        if not self.head.next:
            # no node in the list
            raise RuntimeError("there is no element in the list, cannot remove_from_head")
        headContent = self.head.next.content
        temp = self.head.next.next
        if temp:
            # more than one element in the original list
            self.head.next.prev = None
            self.head.next.next = None
            self.head.next = temp
            temp.prev = self.head
        else:
            # there is only one element in the original list, after remove, there will be no element
            del self.head.next
            self.head.next = None
            self.tail = None
        self.size -= 1
        return headContent

    def move_node_to_head(self, node):
        if self.head.next != node:
            node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev
            else:
                self.tail = node.prev

            node.next = self.head.next
            self.head.next.prev = node
            self.head.next = node
            node.prev = self.head

    def remove_node(self, node):
        node.prev.next = node.next
        if self.tail == node:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        self.size -= 1
        return node

    def move_node_to_tail(self, node):
        if self.tail != node:
            node.prev.next = node.next
            node.next.prev = node.prev
            node.prev = self.tail
            self.tail.next = node
            node.next = None
            self.tail = node

    def set_node_id(self, node, id):
        node.id = id

    def get_head_content(self):
        return self.head.next.content

    def get_tail_content(self):
        return self.tail.content

    def __iter__(self):
        self.currentNode = self.head
        return self

    def next(self):
        return self.__next__()

    def __next__(self):  # Python 3
        if self.currentNode.next is None:
            # self.currentNode = self.head
            raise StopIteration
        else:
            self.currentNode = self.currentNode.next
            return self.currentNode

    def __repr__(self):
        return "linked list"
