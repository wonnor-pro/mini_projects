class myStack:

    def __init__(self):
        self.data = []
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def push(self, object):
        self.data.append(object)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.data.pop()

    def peep(self):
        if self.is_empty():
            return None
        else:
            return self.data[-1]

    def remove_object(self, object):

        if self.is_empty():
            raise RuntimeError("The stack is empty.")
        else:
            if object in self.data:
                self.data.remove(object)
            else:
                raise RuntimeError("Object is not in tge stack.")



