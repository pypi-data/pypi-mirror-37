
## objopt
This library provides object oriented optimization. This allows...

1. using theoretic values (such as the strong convexity parameter)
2. object-oriented definitions, both for models and optimization algorithms. This allows...
    * interacting with the optimization as an object. Want to compute some
      value partway through? Want to change the values as time goes on?
    * getting results intermediately (or in the presence of a keyboard
      interrept)
    * having callbacks, etc

A typical example:

``` python
def get_stats():
    # ...

model = Model()
opt = SGD(model.loss)

data = []
for _ in range(10):
    opt.step(steps=10)
    data += [get_stats(model)]
```

