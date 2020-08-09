class PQueue:

    def __init__(self):
        self.heap_size = 0
        self.heap = []
        self.map = {}

    def is_empty(self):

        # Check if the queue is empty
        return self.heap_size == 0

    def clear(self):

        # Clear the queue
        self.heap_size = 0
        self.heap = []
        self.map = {}

    def size(self):

        # Return the heap_size
        return self.heap_size

    def peek(self):

        # If empty, return None value
        if self.is_empty():
            return None

        # Otherwise, return the first node value
        # without pop it out
        else:
            return self.heap[0]

    def poll(self):

        # If empty, raise runtime error
        if self.is_empty():
            raise RuntimeError("The priority queue is empty.")

        # Otherwise, return the value of the first node
        # and remove it from the queue
        else:
            res = self.heap[0]
            self.remove_at(0)
            return res

    def remove(self, object, index=None):
        if self.is_empty():
            raise RuntimeError("The priority queue is empty.")
        elif not self.contains(object):
            raise RuntimeError("The object is not in the Priority Queue.")
        else:

            if self.heap_size == 1:
                tmp = self.heap[-1]
                self.clear()
                return tmp

            tmp = self.heap[-1]
            self.swap(object, tmp, index, self.heap_size - 1)

            self.heap.pop()
            self.map_remove(object, self.heap_size - 1)
            self.heap_size -= 1

            if not self.sink(tmp, index):
                self.swim(tmp, index)

    def contains(self, object):

        # Check if object is in the queue
        return object in self.map

    def validate_input(self, object, index=None):

        # Check if the object is in the queue
        if not object in self.map:
            raise RuntimeError("Object is not in the queue.")

        # Check if the index matches the record
        else:
            # If no index specified, get a valid value
            if index == None:
                index = self.map_get(object)
            # Otherwise check if index is recorded
            else:
                if not index in self.map[object]:
                    raise RuntimeError("Input index does not match the record.")

        return index

    def add(self, object):

        # Add the object to the last position
        self.heap.append(object)
        # Update the map
        self.map_add(object, self.heap_size)
        # Bubble up the node to meet the heap invariance
        self.swim(object, self.heap_size)
        # Update the heap size
        self.heap_size += 1

    def sink(self, object, index=None):

        # Check the given object and index
        index = self.validate_input(object, index)

        # Calculate the left and right children's index
        left = 2 * index + 1
        right = 2 * index + 2

        # If the node has both child
        if left < self.heap_size and right < self.heap_size:

            # Pick the smaller one
            min_object, min_index = [(self.heap[left], left), (self.heap[right], right)][
                self.heap[left] > self.heap[right]]
            # Check the invariance, if swap is required
            if object > min_object:
                # Swap the node and its child
                self.swap(object, min_object, index, min_index)
                # Keep sinking the node, but the index
                # has been changed to the child's index
                self.sink(object, min_index)
                # Return the operation result
                return True

        # If the node only has one child (i.e. left)
        elif left < self.heap_size:
            if object > self.heap[left]:
                self.swap(object, self.heap[left], index, left)
                self.sink(object, left)
                # Return the operation result
                return True

        # If no operation is needed, return false
        return False

    def swim(self, object, index=None):

        # Check the given object and index
        index = self.validate_input(object, index)

        # Calculate its parent's index
        top = (index - 1) // 2

        # Check if the swap is needed
        if top > 0 and object < self.heap[top]:
            self.swap(object, self.heap[top], index, top)
            # the sequential swim has an updated index
            self.swim(object, top)

            # If any operation has been done, return True
            return True

        # If no operations, return False
        return False

    def swap(self, obj_a, obj_b, index_a=None, index_b=None):

        # Check the given object and index
        index_a = self.validate_input(obj_a, index_a)
        index_b = self.validate_input(obj_b, index_b)

        # Swap the map records
        self.map_swap(obj_a, obj_b, index_a, index_b)

        # Swap the heap
        self.heap[index_a] = obj_b
        self.heap[index_b] = obj_a

    def remove_at(self, index):

        # Check if the index is valid
        if index >= self.heap_size:
            raise IndexError("Index out of range.")

        # Remove the specified object
        else:
            self.remove(self.heap[index], index=index)

    def is_min_heap(self):

        # Calculate the nodes that has child(s)
        check_range = (self.heap_size - 1) // 2

        # Check each parent
        for i in range(check_range + 1):
            # Left kid must exist
            if self.heap[i] > self.heap[2 * i + 1]:
                return False
            # Check if right kid exists
            if 2 * i + 2 < self.heap_size:
                if self.heap[i] > self.heap[2 * i + 2]:
                    return False

        # All parents are valid,
        # then the queue is valid
        return True

    def map_add(self, object, index):

        # If object already exists,
        # add new values
        if object in self.map:
            self.map[object].append(index)

        # Otherwise, create new entry
        else:
            self.map[object] = [index]

    def map_remove(self, object, index):

        # Check the given object and index
        index = self.validate_input(object, index)

        # If only one values found,
        # delete the record
        if len(self.map[object]) == 1:
            del self.map[object]

        # If multiple values are found,
        # delete one entry
        else:
            self.map[object].remove(index)

    def map_get(self, object):

        # If the object is in the map
        # return the first record
        if object in self.map:
            return self.map[object][0]

        # Otherwise return -1
        else:
            return -1

    def map_swap(self, obj_a, obj_b, index_a, index_b):

        # Check the given object and index
        index_a = self.validate_input(obj_a, index_a)
        index_b = self.validate_input(obj_b, index_b)

        # Swap the map records
        self.map[obj_a].remove(index_a)
        self.map[obj_b].remove(index_b)
        self.map[obj_a].append(index_b)
        self.map[obj_b].append(index_a)

    def __str__(self):

        # Print out the heap in levels:
        # ======== HEAP =========
        # [0] 2
        # [1] 7 2
        # [2] 7 13 11 2
        # =======================

        # Calculate total levels
        level = 1
        while 2 ** level < self.heap_size + 1:
            level += 1

        # First row
        res = "======== HEAP =========\n"
        count = 0

        # Each row starts with a level indicator
        for i in range(level):
            res += f"[{i}] "

            # Each element
            for _ in range(2 ** i):
                if count >= self.heap_size:
                    break
                res += f"{self.heap[count]} "
                count += 1

            # Finish one row, start a new line
            res += "\n"

        # End with the line
        res += "======================="

        return res

    def sort(self):

        # poll the queue to generate
        # the sequence of elements
        # in ascending order.
        res = []
        while not self.is_empty():
            res.append(self.poll())

        return res

    def add_from_list(self, lis):

        # Take values from the list,
        # and add them to the queue
        for object in lis:
            self.add(object)

    def sort_list(self, lis):

        # Sort the given
        self.add_from_list(lis)
        return self.sort()


def main():
    my_queue = PQueue()
    b = [2, 7, 11, 7, 13, 2, 2, 3]
    print(b)
    print(my_queue.sort_list(b))
    my_queue.add_from_list(b)
    print(my_queue)


if __name__ == '__main__':
    main()
