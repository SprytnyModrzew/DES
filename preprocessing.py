import math


def preprocess_yuv(ya, yb, ua, ub, va, vb):
    len_y = len(yb)
    m = len_y
    xor_y = []
    for i in range(len_y):
        xor_y[i] = ya[i] ^ yb[m]
        m = m-1

    len_u = len(ub)
    m = len_u
    xor_u = []
    xor_v = []
    for i in range(len_u):
        xor_u[i] = ua[i] ^ ub[m]
        xor_v[i] = va[i] ^ vb[m]
        m = m-1

    z = []
    for i in range(2*len_u):
        if i % 2 == 0:
            z[2*i] = xor_y[i]
            z[(2*i)+1] = xor_u[i]
        else:
            z[2*i] = xor_y[i]
            z[(2*i)+1] = xor_v[math.floor(i/2)]

    len_z = len_y+(2*len_u)
    e = 2*len_u
    for i in range(4*len_u, len_z):
        z[i] = xor_y[e]
        e = e+1

    return z


def preprocess_rgb(r1, g1, b1, r2, g2, b2):
    length = len(r2)
    m = length-1
    xor_r = []
    xor_g = []
    xor_b = []
    for i in range(length):
        xor_r.append(r1[i] ^ r2[m])
        xor_g.append(g1[i] ^ g2[m])
        xor_b.append(b1[i] ^ b2[m])
        m = m-1

    z = []
    for i in range(length):
        z.append(xor_r[i])
        z.append(xor_g[i])
        z.append(xor_b[i])

    return z
