
import numpy as np


def illmat(D, random_state=None):
    """Generate a <D x D> ill-conditioned correlation matrix
    with random coefficients

    Parameters:
    -----------
    D : int
        Dimension of the matrix

    Return:
    -------
    cmat : ndarray
        DxD matrix with +1 as diagonal elements,
        mirrored random numbers [-1,+1].
    """
    if random_state:
        np.random.seed(random_state)

    uni = np.random.uniform(size=(D, D))

    tmp = np.minimum(1., np.maximum(-1., 2 * uni - 1.0))

    tmp = np.triu(tmp, k=1)

    return np.eye(D) + tmp + tmp.T
