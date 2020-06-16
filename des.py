import sys

from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication,
                             QVBoxLayout, QDialog, QLabel, QFormLayout, QGroupBox, QPlainTextEdit,
                             QHBoxLayout, QRadioButton)
from bitarray import bitarray


class Keys:
    def __init__(self):
        f = open('numbers.txt', "r")
        self.lines_all = list(f)
        self.current = 0

    def get_next_key(self):
        self.current += 1
        return self.lines_all[self.current]


permutation_start = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
                     62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
                     57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
                     61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
permutation_end = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
                   38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
                   36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
                   34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
expansion = [32, 1, 2, 3, 4, 5,
             4, 5, 6, 7, 8, 9,
             8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32, 1]
PC1 = \
    [57, 49, 41, 33, 25, 17, 9,
     1, 58, 50, 42, 34, 26, 18,
     10, 2, 59, 51, 43, 35, 27,
     19, 11, 3, 60, 52, 44, 36,
     63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
     14, 6, 61, 53, 45, 37, 29,
     21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

permutation = \
    [16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25]

s_box = \
    [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
     [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
     [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
     [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
     [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
     [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
     [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
     [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


def init_permutation(plaintext):
    temp = plaintext.copy()
    for i in range(0, 64):
        plaintext[i] = temp[permutation_start[i] - 1]
    return plaintext


def final_permutation(plaintext):
    temp = plaintext.copy()
    for i in range(0, 64):
        plaintext[i] = temp[permutation_end[i] - 1]
    return plaintext


def pc1_function(key):
    temp = bitarray()
    for i in range(0, 56):
        temp.append(key[PC1[i] - 1])
    return temp


def pc2_function(key):
    temp = bitarray()
    for i in range(0, 48):
        temp.append(key[PC2[i] - 1])
    return temp


def leftshift(ba, count):
    x = ba
    while count:
        x = x[1:] + (bitarray('0'))
        if ba[0] == 1:
            x[-1] = True
        count -= 1
        ba = x
    return x


def rightshift(ba, count):
    x = ba
    while count:
        x = (bitarray('0')) + ba[:-1]
        if ba[-1] == 1:
            x[0] = True
        count -= 1
        ba = x
    return x


def rotate(key, flip, mode):
    c = key[0:28]
    d = key[28:56]
    if mode:
        return bitarray(leftshift(c, flip) + leftshift(d, flip))
    else:
        return bitarray(rightshift(c, flip) + rightshift(d, flip))


def expansion_function(r):
    temp = bitarray()
    for i in range(0, 48):
        temp.append(r[expansion[i] - 1])
    return temp


def permutation_function(r):
    temp = bitarray()
    for i in range(0, 32):
        temp.append(r[permutation[i] - 1])
    return temp


def s_box_substitution(number, r):
    column = 0
    row = 0
    if r[0]:
        row += 2
    if r[-1]:
        row += 1
    if r[1]:
        column += 8
    if r[2]:
        column += 4
    if r[3]:
        column += 2
    if r[4]:
        column += 1
    return s_box[number][row][column]


def f_function(r, k):
    temp_r = expansion_function(r)
    temp_r = temp_r ^ k
    substituted = bitarray()
    for i in range(0, 8):
        temp = s_box_substitution(i, temp_r[6 * i:(6 * i + 6)])
        if temp & 8:
            substituted.append(True)
        else:
            substituted.append(False)
        if temp & 4:
            substituted.append(True)
        else:
            substituted.append(False)
        if temp & 2:
            substituted.append(True)
        else:
            substituted.append(False)
        if temp & 1:
            substituted.append(True)
        else:
            substituted.append(False)
    return permutation_function(substituted)


def encrypt(plaintext, encryption_key):
    plaintext = init_permutation(plaintext)
    left = plaintext[0:32]
    right = plaintext[32:64]
    encryption_key = pc1_function(encryption_key)
    y = encryption_key
    for i in range(0, 16):
        if i == 0 or i == 1 or i == 8 or i == 15:
            flips = 1
        else:
            flips = 2
        y = rotate(y, flips, True)
        x = pc2_function(y)
        temporary_l = left.copy()
        left = right.copy()
        right = temporary_l ^ f_function(right, x)

    combined = final_permutation(bitarray(right.to01() + left.to01()))

    return combined


def decrypt(plaintext, decryption_key):
    plaintext = init_permutation(plaintext)

    left = plaintext[0:32]
    right = plaintext[32:64]

    decryption_key = pc1_function(decryption_key)
    y = decryption_key
    for i in range(0, 16):
        if i == 0:
            flips = 0
        elif i == 1 or i == 8 or i == 15:
            flips = 1
        else:
            flips = 2
        y = rotate(y, flips, False)
        x = pc2_function(y)
        temporary_l = left.copy()
        left = right.copy()
        right = temporary_l ^ f_function(right, x)

    combined = final_permutation(bitarray(right.to01() + left.to01()))
    return combined


def pack_string(string_input):
    t = bitarray()
    t.frombytes(string_input.encode('utf-8'))
    temp_list = []
    for i in range(0, int(t.length() / 64) + 1):
        temp = t[i * 64:i * 64 + 64]
        if temp.length() < 64:
            temp = bitarray("0") * (64 - temp.length()) + temp
        temp_list.append(temp)
    return temp_list


def pack_key(key_to_pack):
    b = [key_to_pack >> i & 1 for i in range(63, -1, -1)]
    return bitarray(b)


def pack_hex(hex_to_pack):
    b = [hex_to_pack >> i & 1 for i in range(7, -1, -1)]
    return bitarray(b)


class Crypt(QDialog):
    def action_crypt(self):
        return

    def get_key(self):
        return

    def __init__(self, parent=None):
        super(Crypt, self).__init__(parent)
        self.plain_text_entry = QPlainTextEdit()
        self.plain_text_label = QLabel()
        self.button_crypt = QPushButton()
        self.plain_text_label_result = QLabel()
        self.plain_text_result = QPlainTextEdit()
        self.layout_main = QVBoxLayout()
        self.checkboxes = QGroupBox()
        self.radio_button_binary = QRadioButton("Binary")
        self.radio_button_hex = QRadioButton("Hex")
        self.h_box = QHBoxLayout()
        self.radio_button_binary.setChecked(True)
        self.h_box.addWidget(self.radio_button_binary)
        self.h_box.addWidget(self.radio_button_hex)
        self.checkboxes.setLayout(self.h_box)

        self.key_form = QFormLayout()
        self.key_form_button = QPushButton("Get new key")
        self.key_form_label = QLabel("Key:")
        self.key_form_label2 = QLabel("Key:")
        self.key_form_line = QLineEdit()
        self.key_form.addRow(self.key_form_label, self.key_form_button)
        self.key_form.addRow(self.key_form_label2, self.key_form_line)

        self.layout_main.addLayout(self.key_form)

        self.layout_main.addWidget(self.plain_text_label)
        self.layout_main.addWidget(self.plain_text_entry)
        self.layout_main.addWidget(self.checkboxes)
        self.layout_main.addWidget(self.plain_text_label_result)
        self.layout_main.addWidget(self.plain_text_result)
        self.layout_main.addWidget(self.button_crypt)
        self.setLayout(self.layout_main)

        self.plain_text_result.hide()
        self.plain_text_label_result.hide()

        self.button_crypt.clicked.connect(self.action_crypt)
        self.key_form_button.clicked.connect(self.get_key)
        self.plain_text_result.setReadOnly(True)


class Decrypt(Crypt):
    def action_crypt(self):
        if self.radio_button_hex.isChecked():
            x = bytes.fromhex(self.plain_text_entry.toPlainText())
            xy = bitarray()
            for i in range(0, len(x)):
                xy = xy + pack_hex(x[i])

        else:
            xy = bitarray(self.plain_text_entry.toPlainText())

        the_key = pack_key(int(self.key_form_line.text()))

        string_text = ""
        for i in range(0, int(len(xy) / 64)):
            uuu = decrypt(xy[i * 64:i * 64 + 64], the_key)
            string_text += uuu.to01()

        self.plain_text_result.show()
        self.plain_text_result.setPlainText(bitarray(string_text).tostring())
        self.plain_text_label_result.show()

    def __init__(self, parent=None):
        super(Decrypt, self).__init__(parent)
        self.setWindowTitle("Decrypt")
        self.plain_text_label.setText("Input to decrypt")
        self.plain_text_label_result.setText("Result:")
        self.button_crypt.setText("Decrypt")
        self.key_form_label.hide()
        self.key_form_button.hide()


class Encrypt(Crypt):
    def action_crypt(self):
        lis = pack_string(self.plain_text_entry.toPlainText())

        the_key = pack_key(int(self.key_int))

        string_text = ""
        for e in range(0, len(lis)):
            uuu = encrypt(lis[e], the_key)
            string_text += uuu.to01()
        if self.radio_button_hex.isChecked():
            self.plain_text_result.setPlainText(bitarray(string_text).tobytes().hex())
        else:
            self.plain_text_result.setPlainText(bitarray(string_text).to01())
        self.plain_text_result.show()
        self.plain_text_label_result.show()

    def get_key(self):
        self.key_int = self.key.get_next_key()
        self.key_form_label.setText("Key:" + str(self.key_int))

    def __init__(self, parent=None):
        super(Encrypt, self).__init__(parent)
        self.key = Keys()
        self.key_int = self.key.get_next_key()
        self.setWindowTitle("Encrypt")
        self.plain_text_label.setText("Text to encrypt")
        self.plain_text_label_result.setText("Result:")
        self.button_crypt.setText("Encrypt")
        self.key_form_label.setText("Key:" + str(self.key_int))
        self.key_form_label2.hide()
        self.key_form_line.hide()


class Form(QDialog):
    def encrypt(self):
        self.encrypt_win.show()

    def decrypt(self):
        self.decrypt_win.show()

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.decrypt_win = Decrypt()
        self.encrypt_win = Encrypt()
        self.setWindowTitle("Menu")
        self.setMinimumWidth(200)
        self.button = QPushButton("Encrypt")
        self.button2 = QPushButton("Decrypt")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

        self.button.clicked.connect(self.encrypt)
        self.button2.clicked.connect(self.decrypt)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()

    sys.exit(app.exec_())
