class doublyLinked:

    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    class node():
        def __init__(self, data, previous_node = None, next_node = None):
            self.data = data
            self.next = next_node
            # Set the previous node of the head as itself
            self.previous = previous_node if previous_node else self

        def __str__(self):
            return str(self.data)

        def clear_previous(self):
            # Set the previous node of the head as itself
            self.previous = self

        def clear_next(self):
            # Set the next node of the tail as None
            self.next = None

    def __str__(self):

        # Define the print format of the data structure
        # E.g. Doubly Linked Chain: 6 <-> 4 <-> 98 <-> 50
        res = "Doubly Linked Chain: "
        node = self.head
        while node:
            # Skip the first <->
            if node == self.head:
                res += str(node)
            else:
                res += ' <-> ' + str(node)
            node = node.next
        return res

    def clear(self):

        self.length = 0
        self.head = None
        self.tail = None

    def size(self):
        return self.length

    def add_last(self, data):

        # If the Data structure is empty, then set both the head and the tail
        # as the new node created.
        if self.is_empty():
            new_node = self.node(data, previous_node=self.tail, next_node=None)
            self.head = new_node
            self.tail = new_node
        else:
            new_node = self.node(data, previous_node=self.tail, next_node=None)
            # Connect the new node to the tail
            self.tail.next = new_node
            # Set the new_node as the new tail
            self.tail = new_node

        self.length += 1

    def add_first(self, data):

        # If the Data structure is empty, then set both the head and the tail
        # as the new node created.
        if self.is_empty():
            new_node = self.node(data, previous_node=None, next_node=self.head)
            self.tail = new_node
            self.head = new_node
        else:
            new_node = self.node(data, previous_node=None, next_node=self.head)
            # Connect the new node to the head
            self.head.previous = new_node
            # Set the head as the new node
            self.head = new_node

        self.length += 1

    def peek_first(self):

        # Raise error if it is empty
        if self.is_empty():
            raise RuntimeError("The data structure is empty.")
        else:
            # return the data of the head
            return self.head.data

    def peek_last(self):

        # Raise error if it is empty
        if self.is_empty():
            raise RuntimeError("The data structure is empty.")
        else:
            # return the data of the tail
            return self.tail.data

    def remove_first(self):

        # Set the second node to be the head
        self.head = self.head.next
        # Clear the previous node for the new head
        self.head.clear_previous()
        # Update the length
        self.length -= 1

    def remove_last(self):

        # Set the second last node to be the tail
        self.tail = self.tail.previous
        # Clear the next node for the new tail
        self.tail.clear_next()
        # Update the length
        self.length -= 1

    def remove_node(self, node):

        # Call existing methods for the two special cases
        if self.head == node:
            self.remove_first()
        elif self.tail == node:
            self.remove_last()
        # A node in the middle
        else:
            # Connect the previous node with the next node
            node.previous.next = node.next
            node.next.previous = node.previous
            # Update the length
            self.length -= 1

    def remove_at(self, index):

        # Check if the index is valid
        if index >= self.length:
            raise IndexError("Index out of range.")
        else:
            # Locate the target node
            count = 0
            node = self.head
            while count < index:
                node = node.next
                count += 1
            # Remove the target node
            self.remove_node(node)

    def remove_object(self, object):

        # Check if it is empty
        if self.is_empty():
            raise RuntimeError("The data structure is empty.")
        else:
            # Check if the data matches the target, if so, remove the node
            # Note: it will only remove the first target it sees
            node = self.head
            while node:
                if node.data == object:
                    self.remove_node(node)
                    break
                node = node.next

    def index_of(self, object):

        # The object is not in it, return -1
        if self.is_empty():
            return -1
        else:
            # Initialise a list
            res = []
            node = self.head
            count = 0
            while node:
                # Add the index to the results
                # list if the data matches
                if node.data == object:
                    res.append(count)
                node = node.next
                count += 1
            # If no matches found, return -1
            if not res:
                return -1
            # If only one matches found,
            # return the index as int
            elif len(res) == 1:
                return res[0]
            # If more than one matches found,
            # return the index in the list
            else:
                return res

    def contains(self, object):

        # Empty chains contain no object.
        if self.is_empty():
            return False
        else:
            node = self.head
            while node:
                # If there exist matches,
                # return True
                if node.data == object:
                    return True
                node = node.next
            # If tno matches found,
            # return False
            return False

    def is_empty(self):

        # Check if the data structure is empty
        if not self.head:
            return True
        else:
            return False


def main():
    a = doublyLinked()
    a.add_last(98)
    a.add_first(4)
    a.add_first(6)
    a.add_last(50)
    print(a)
    a.remove_at(2)
    a.remove_object(4)
    a.add_last(28)
    a.add_last(60)
    a.add_first(4)
    a.add_first(6)
    a.add_last(60)
    print(a)
    print("The index of 60:", a.index_of(60))
    print("The index of 80:", a.index_of(80))
    print("If it contains 50:", a.contains(50))


if __name__ == '__main__':
    main()