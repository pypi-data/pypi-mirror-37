import numpy as np
import numpy.linalg as LA
from losses import LeastSquaresL2Reg, LogisticLoss

np.random.seed(42)

def _make_inputs(n, d, seed=42):
    A = np.random.randn(n, d)
    x_star = np.random.randn(d)
    return A, x_star


def test_logit_loss(n=1000, d=10):
    A, x_star = _make_inputs(n, d)
    y = np.sign(A @ x_star)

    model = LogisticLoss(A, y)

    X = [np.random.randn(d) for i in range(100)]
    for i, x in enumerate(X):
        y_hat = model.predict(A, x)
        y = model.predict(A, x_star)
        errors = np.abs(y - y_hat) / 2
        assert errors.sum() > 0

        g_x = model.grad(A, y, x)
        g_star = model.grad(A, y, x_star)
        assert LA.norm(g_star) < LA.norm(g_x)

if __name__ == "__main__":
    test_logit_loss()
