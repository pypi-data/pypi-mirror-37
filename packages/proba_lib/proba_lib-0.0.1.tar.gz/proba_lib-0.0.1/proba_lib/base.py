from abc import ABC, abstractmethod

class BaseEvent(ABC):

    def __invert__(self):
        return op.Inversion(self)

    def __and__(self, other):
        return op.Join(self, other)

    def __or__(self, other):
        return op.Condition(self, other)


    @abstractmethod
    def __call__(self, table):
        pass

class BaseOperation(BaseEvent):
    def __init__(self, *events, **kwargs):
        super(BaseOperation, self).__init__()
        self.events = events

    def __repr__(self):
        return self._repr_fmt.format(op=self.operation, *self.events)

    @property
    @abstractmethod
    def _repr_fmt(self):
        pass

import proba_lib.operations as op
