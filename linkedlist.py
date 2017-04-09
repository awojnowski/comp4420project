import math

class LinkedList():
    def __init__(self, values):
        length = len(values)
        skip_length = int(math.floor(math.sqrt(length)))

        values_list = []
        skips_list = []
        skip_total = 0
        skip_position = skip_length
        for i in xrange(length):
            if i == skip_position:
                skip_position = min(skip_position + skip_length, length)
            values_list.append(values[i])
            skips_list.append(skip_position)
        self.values_list = values_list
        self.skips_list = skips_list
        self.position = 0


    def index(self):
        return self.position


    def fetch(self):
        return self.values_list[self.position]


    def has_item(self):
        if self.position >= len(self.values_list):
            return False
        return True


    def next(self):
        self.position += 1


    def previous(self):
        self.position -= 1


    def skip(self):
        self.position = self.skips_list[self.position]