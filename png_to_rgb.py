from PIL import Image


def png_to_rgb(im_path):
    im = Image.open(im_path)
    rgb_im = im.convert('RGB')
    width, height = im.size
    # print(width)
    r_list = []
    g_list = []
    b_list = []
    for i in range(0, int(width)):
        for j in range(0, int(height)):
            r, g, b = rgb_im.getpixel((i, j))
            r_list.append(r)
            g_list.append(g)
            b_list.append(b)
            # print(str(i)+"  "+str(j))
    return r_list, g_list, b_list
