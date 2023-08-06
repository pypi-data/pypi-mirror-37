from warnings import warn
import numpy as np
import numpy.linalg as LA


class SGD:
    def __init__(self, model):
        self.model = model
        assert len(model.A) == len(model.y), "Number of examples"
        self.est = np.random.randn(self.model.d)
        self.epochs = 0
        self.steps = 0
        self.name = 'SGD'

    def _run_batch(self, step_size=None, batch_size=100):
        if step_size is None:
            step_size = self.step_size
            #  step_size *= batch_size / self.model.n

        self.epochs += batch_size / self.model.n
        self.steps += 1
        i = np.random.permutation(self.model.n)[:batch_size]
        self.est -= step_size * self.model.grad(self.model.A[i], self.model.y[i], self.est)

    def run(self, n_steps=100, **kwargs):
        for _ in range(n_steps):
            self._run_batch(**kwargs)

    @property
    def step_size(self):
        return 1 / self.model.lipschitz


def _est_variance(l):
    return sum(l) / (len(l) - 1)


class BigBatch(SGD):
    def __init__(self, model):
        super(BigBatch, self).__init__(model)
        self.batch_size = 0
        self.name = 'BigBatch'

    def get_batch(self, x, batch_increment=10):
        A = self.model.A
        y = self.model.y
        i = np.random.permutation(self.model.n)
        if self.batch_size == 0:
            self.batch_size = batch_increment
        batch = i[:self.batch_size]
        grads = [self.model.grad(a, yi, x) for a, yi in zip(A[batch], y[batch])]
        while True:
            new_batch = i[self.batch_size:self.batch_size + batch_increment]
            grads += [self.model.grad(a, yi, x)
                      for a, yi in zip(A[new_batch], y[new_batch])]
            self.batch_size += batch_increment
            batch = i[:self.batch_size]

            batch_grad = self.model.grad(self.model.A[batch], self.model.y[batch], x)
            V = _est_variance([LA.norm(g - batch_grad)**2 for g in grads])
            if LA.norm(batch_grad)**2 > V / self.batch_size:
                break
        return batch

    def _run_batch(self, step_size=None, **kwargs):
        if 'batch_size' in kwargs:
            warn('BigBatch estimates batch size; batch_size ignored')
        i = self.get_batch(self.est)
        batch_size = len(i)
        if step_size is None:
            step_size = self.step_size
            step_size *= batch_size / self.model.n

        self.epochs += batch_size / self.model.n
        self.steps += 1
        self.est -= step_size * self.model.grad(self.model.A[i], self.model.y[i], self.est)
