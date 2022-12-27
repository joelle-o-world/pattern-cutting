class Abstract_Group:
    def __init__(self, *objects, label=None, **named_objects):
        self.objects = {}
        for key in named_objects:
            self[key] = named_objects[key]
        for object in objects:
            self.append(objects)

    def new_unused_key(self, prefix="unlabeled_"):
        i = 0
        while "{}{}".format(prefix, i) in self.objects:
            i += 1
        return "{}{}".format(prefix, i)

    def __getitem__(self, key: str):
        return self.objects[key]
    def __setitem__(self, key: str, value):
        self.objects[key ] = value
    def __delitem__(self, key):
        del self.objects[key]
    def append(self, obj):
        self.objects[self.new_unused_key()] = obj

    def iterate_objects(self):
        for key in self.objects:
            yield self.objects[key]
