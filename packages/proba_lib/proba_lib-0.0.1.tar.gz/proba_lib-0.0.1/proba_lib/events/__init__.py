from proba_lib.base import BaseEvent

class BinaryEvent(BaseEvent):
    def __init__(self, name, children=[]):
        super(BinaryEvent, self).__init__()
        self.name = name
        self.children = children

        stack = list(children)
        self.all_children = []

        while stack:
            child = stack.pop()
            if child.children:
                stack.extend(child.children)
            else:
                self.all_children.append(child)

    def __repr__(self):
        return "<BinaryEvent \"{}\">".format(self.name)

    @classmethod
    def new(cls, names, *args, **kwargs):
        return [cls(name, *args, **kwargs) for name in names]

    def __call__(self, table):
        assert self in table.events, \
            "Unknown event object: {}".format(self)

        i = table.event_index[self]
        return table.values[:, i]
