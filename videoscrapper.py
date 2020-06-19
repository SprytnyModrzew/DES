import cv2


def get_image():
    camera = cv2.VideoCapture(0)
    for i in range(2):
        return_value, image = camera.read()
        cv2.imwrite('tests/img' + str(i) + '.png', image)
    del camera
