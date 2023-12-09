import numpy as np


def chinese_remainder(a, n):
    # x = a_i ( mod n_i )
    # x = sum_i prod_j i!=j n_j * m_i
    #   = sum_i b_i m_i
    # where b_i * m_i % n_i = a_i
    assert len(a) == len(n)
    N = np.prod(n)
    b = [N / n_i for n_i in n]
    a = [a_i % n_i for a_i, n_i in zip(a, n)]
    m = []
    for i in range(len(a)):
        m_i = 1
        b_i = b[i]
        n_i = n[i]
        a_i = a[i]
        while (b_i * m_i) % n_i != a_i:
            m_i += 1
        m.append(m_i)
    x = sum([b_i * m_i for b_i, m_i in zip(b, m)])
    return x % N
