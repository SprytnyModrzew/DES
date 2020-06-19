import math

import preprocessing
import postprocessing
import png_to_rgb


def get_rgb():
    r1, g1, b1 = png_to_rgb.png_to_rgb("tests/img40.png")
    r2, g2, b2 = png_to_rgb.png_to_rgb("tests/img41.png")
    z = preprocessing.preprocess_rgb(r1, g1, b1, r2, g2, b2)
    # print("Entropy before postprocessing:")
    # print(entropy.entropy_calc(z, 256))
    # histogram.make_hist(z)
    z = z[0:math.floor(len(z))]
    return z


def get_rng(z):
    generator = postprocessing.postprocess(
        z[0:math.floor(len(z))], 6, 3.9 + 0 / (10.01 * 3))

    while True:
        try:
            xorbytearray = generator.__next__()
            byte_memory = memoryview(xorbytearray)
            byte_list = [sum([byte[b] << b for b in range(0, 32)])
                         for byte in zip(*(iter(byte_memory),) * 32)]
            for i in byte_list:
                yield i
        except StopIteration:
            # get new generator
            break
    print("finito")