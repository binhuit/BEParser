class HashTable:
    """
    A dict used to index item in list
    """

    def __init__(self):
        # item store item as key and index as value
        # indexes store index as key and item as value
        self.items = {}
        self.indexes = {}
        self.count = 0

    def add(self, item):
        if not item in self.items:
            self.items[item] = self.count
            self.indexes[self.count] = item
            self.count += 1

    def get_index(self, item):
        self.add(item)
        return self.items[item]

    def get_value(self, index):
        try:
            return self.indexes[index]
        except KeyError:
            print "Item did not index yet"
            raise

    def __len__(self):
        return self.count

    def save_file(self, filename):
        with open(filename, 'w') as f:
            for i in xrange(self.count):
                f.write(self.indexes[i]+"\n")


