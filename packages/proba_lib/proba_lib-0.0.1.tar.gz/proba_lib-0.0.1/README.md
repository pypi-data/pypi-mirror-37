# Probability Library

## Simple Example

```python
from proba_lib import BinaryEvent, ProbaTable
import numpy as np

# all combinations for 3 variables
combinations = np.array([list(map(int, "{:03b}".format(i))) for i in range(2**3)])
predictions = np.array([1,1,0,1,1,0,1,0]).reshape(-1, 1)

events = x0, x1, x2, y = BinaryEvent.new("x0 x1 x2 y".split())

P = ProbaTable(events, np.hstack([combinations, predictions]))
print([e.name for e in P.events])
# ['x0', 'x1', 'x2', 'y']

print(P.values.astype(int))
#[[0 0 0 1]
# [0 0 1 1]
# [0 1 0 0]
# [0 1 1 1]
# [1 0 0 1]
# [1 0 1 0]
# [1 1 0 1]
# [1 1 1 0]]

# The Bayes' Rule
print(P(y | x0) * P(x0) == P(x0 | y) *  P(y))
# True

print(P(y | x0))
# 0.4

print(P(x0 | y))
# 0.4

print(P(x0 & x1 | y))
# 0.2
```
