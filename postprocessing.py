import math

from bitstring import BitStream


def postprocess(z, lattice, init_r):
    def logistic_map(map_x, r_list, index_r, index_r2):
        if map_x == 0:
            map_x = r_list[index_r][index_r2] / 4
        r_list[index_r][index_r2] = r_list[index_r][index_r2] + \
            (0.001 * map_x) + c
        if r_list[index_r][index_r2] > 4:
            r_list[index_r][index_r2] = 3.9 + \
                (0.0025 * r_list[index_r][index_r2])
        for _ in range(50):
            map_x = r_list[index_r][index_r2] * map_x * (1 - map_x)
        return map_x, r_list[index_r][index_r2]

    byte_array = bytearray()
    j = 0
    x = []
    r = []
    for i in range(lattice):
        r.append([init_r for j in range(lattice)])
        x.append([0 for j in range(lattice)])
    c = 0.002
    epsilon = 0.5
    length_z = len(z)
    while j < len(z):
        for i in range(lattice):
            x[i][0] = (z[(i + j) % length_z] - min(z)) / (max(z) - min(z))
        for t in range(math.floor((lattice / 2))):
            for i in range(lattice):
                map1, r[i][t + 1] = logistic_map(x[i][t], r, i, t)
                map2, r[(i + 1) % lattice][t + 1] = logistic_map(x[(i + 1) %
                                                                   lattice][t], r, (i + 1) % lattice, t)
                map3, r[(i - 1) % lattice][t - 1] = logistic_map(x[(i - 1) %
                                                                   lattice][t], r, (i - 1) % lattice, t)
                x[i][t + 1] = ((epsilon * map1) +
                               ((epsilon / 2) * map2) + map3) % 1
        for i in range(lattice):
            bs = BitStream(
                float=x[i][math.floor((lattice / 2) - 1)], length=64)
            xor = bytes(a ^ b for (a, b) in zip(bs[0: 32], bs[32:]))
            yield bytearray(xor)
        j = j + lattice
