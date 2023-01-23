class Abstract_Group:
    def __init__(self, *unnamed_objects, label=None, **named_objects):
        self.objects = {}
        self.add_objects(*unnamed_objects, **named_objects)

    def new_unused_key(self, prefix="unlabeled_"):
        i = 0
        while "{}{}".format(prefix, i) in self.objects:
            i += 1
        return "{}{}".format(prefix, i)

    def __getitem__(self, key: str):
        return self.objects[key]

    def __setitem__(self, key: str, value):
        self.objects[key] = value

    def __delitem__(self, key):
        del self.objects[key]

    def __str__(self):
        out = "group:\n"
        for key in self.objects:
            out += "\t{} = {}\n".format(key, self.objects[key])
        return out

    def append(self, obj):
        self.objects[self.new_unused_key()] = obj

    def iterate_objects(self):
        for key in self.objects:
            yield self.objects[key]

    def add_objects(self, *unnamed_objects, **named_objects):
        for o in unnamed_objects:
            self.append(o)
        for key in named_objects:
            self.objects[key] = named_objects[key]
        return self
