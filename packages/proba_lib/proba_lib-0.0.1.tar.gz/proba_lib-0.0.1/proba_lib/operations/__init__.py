import numpy as np
from proba_lib.base import BaseOperation

class UnaryOperation(BaseOperation):
    def __init__(self, *args, **kwargs):
        super(UnaryOperation, self).__init__(*args, **kwargs)
        assert len(self.events) == 1, "There should be 1 event!"

    @property
    def _repr_fmt(self):
        return "<Op {op}{0}>"

class BinaryOperation(BaseOperation):
    def __init__(self, *args, **kwargs):
        super(BinaryOperation, self).__init__(*args, **kwargs)
        assert len(self.events) == 2, "There should be 2 events!"

    @property
    def _repr_fmt(self):
        return "<Op {0}{op}{1}>"

class Inversion(UnaryOperation):
    operation="~"

    def __call__(self, table):
        x, = self.events
        return np.logical_not(x(table))

class Join(BinaryOperation):
    operation="&"

    def __call__(self, table):
        x0, x1 = self.events
        return np.logical_and(x0(table), x1(table))

class Condition(BinaryOperation):
    operation="|"

    def __call__(self, table):
        x0, x1 = self.events
        return x0(table)[x1(table)]

