class PQueue:

    def __init__(self):
        self.heap_size = 0
        self.heap = []
        self.map = {}

    def is_empty(self):
        return self.heap_size == 0

    def clear(self):
        self.heap_size = 0
        self.head = []
        self.map = {}

    def size(self):
        return self.heap_size

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.heap[0]

    def poll(self):
        if self.is_empty():
            raise RuntimeError("The priority queue is empty.")
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
        return object in self.map

    def validate_input(self, object, index=None):
        if not object in self.map:
            print(self.map)
            raise RuntimeError("Object is not in the queue.")
        else:
            if index == None:
                index = self.map_get(object)
            else:
                if not index in self.map[object]:
                    print(self.map)
                    raise RuntimeError("Input index does not match the record.")

        return index

    def add(self, object):
        self.heap.append(object)
        self.map_add(object, self.heap_size)
        self.swim(object, self.heap_size)
        self.heap_size += 1

    def sink(self, object, index=None):
        index = self.validate_input(object, index)

        left = 2 * index + 1
        right = 2 * index + 2

        if left < self.heap_size and right < self.heap_size:
            min_object, min_index = [(self.heap[left], left), (self.heap[right], right)][
                self.heap[left] > self.heap[right]]
            # print(object, min_object, min_index)
            if object > min_object:
                self.swap(object, min_object, index, min_index)
                self.sink(object, min_index)
                return True

        return False

    def swim(self, object, index=None):

        index = self.validate_input(object, index)

        top = (index - 1) // 2

        if top > 0 and object < self.heap[top]:
            self.swap(object, self.heap[top], index, top)
            self.swim(object, top)

            return True

        return False

    def swap(self, obj_a, obj_b, index_a=None, index_b=None):

        index_a = self.validate_input(obj_a, index_a)
        index_b = self.validate_input(obj_b, index_b)

        # Swap the map records
        self.map_swap(obj_a, obj_b, index_a, index_b)

        # Swap the heap
        self.heap[index_a] = obj_b
        self.heap[index_b] = obj_a

    def remove_at(self, index):
        if index >= self.heap_size:
            raise IndexError("Index out of range.")
        else:
            self.remove(self.heap[index], index=index)

    def is_min_heap(self):
        check_range = (self.heap_size - 1) // 2
        for i in range(check_range + 1):
            if self.heap[i] > self.heap[2 * i + 1]:
                return False
            if 2 * i + 2 < self.heap_size:
                if self.heap[i] > self.heap[2 * i + 2]:
                    return False

        return True

    def map_add(self, object, index):
        if object in self.map:
            self.map[object].append(index)
        else:
            self.map[object] = [index]

    def map_remove(self, object, index):
        index = self.validate_input(object, index)

        if len(self.map[object]) == 1:
            del self.map[object]
        else:
            self.map[object].remove(index)

    def map_get(self, object):
        if object in self.map:
            return self.map[object][0]
        else:
            return -1

    def map_swap(self, obj_a, obj_b, index_a, index_b):
        index_a = self.validate_input(obj_a, index_a)
        index_b = self.validate_input(obj_b, index_b)

        self.map[obj_a].remove(index_a)
        self.map[obj_b].remove(index_b)
        self.map[obj_a].append(index_b)
        self.map[obj_b].append(index_a)

    def __str__(self):
        return str(self.heap)


def main():
    a = PQueue()
    b = [2, 7, 11, 7, 13, 2, 2]
    for i in b:
        a.add(i)
    print(a)

    a.add(3)
    print(a)

    print(a.is_min_heap())
    while not (a.is_empty()):
        print(a.poll())


if __name__ == '__main__':
    main()
