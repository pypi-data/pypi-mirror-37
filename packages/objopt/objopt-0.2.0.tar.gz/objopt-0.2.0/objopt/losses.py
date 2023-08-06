import numpy as np
import numpy.linalg as LA


class LeastSquaresL2Reg:
    def __init__(self, A, y, lmbda=0.1):
        self.A = A
        self.y = y
        self.n, self.d = A.shape
        self.lmbda = lmbda
        self.strong_cvx = lmbda
        self.singular_values = LA.svd(A, compute_uv=False)

    def _loss(self, a, y, x):
        return (1 / (2*self.n)) * ((a@x - y)**2 + self.lmbda * LA.norm(x)**2)

    def loss(self, A, y, x, return_list=False):
        if return_list:
            return [self._loss(a, yi, x) for a, yi in zip(A, y)]
        return (1 / (2*self.n)) * (LA.norm(A@x - y)**2 + self.lmbda * LA.norm(x)**2)

    def grad(self, A, y, x):
        nb_eg = A.shape[0] if len(A.shape) > 1 else 1
        shape = (nb_eg, -1) if nb_eg > 1 else (1, -1)
        A = A.reshape(*shape)
        r = A@x - y
        return A.T@r/self.n + self.lmbda * x * (nb_eg / self.n)

    def predict(self, A, x):
        return A @ x

    @property
    def lipschitz(self):
        return self.lmbda + max(self.singular_values)**2 / self.n

    @property
    def PL_modulus(self):
        return self.strong_cvx / (2 * self.lipschitz)


class LogisticLoss:
    def __init__(self, A, y):
        self.A = A
        self.y = y
        self.n, self.d = A.shape
        assert set(np.unique(y)) == {-1, 1}

    def _loss(self, a, y, x):
        return np.log(1 + np.exp(-y * np.inner(a, x)))

    def loss(self, A, y, x):
        loss = (1/self.n) * np.array([self._loss(a, yi, x)
                                      for a, yi in zip(A, y)])
        return loss

    def grad(self, A, y, x):
        yAx = y * (A @ x)
        C = -y * np.exp(-yAx) / (1 + np.exp(-yAx))
        # could use numpy broadcasting here; (C * A.T).sum(axis=?)
        return sum(c * a for a, c in zip(A, C))

    def predict(self, A, x):
        return np.sign(A @ x)



