import numpy as np
import math
import warnings

from encoding import TextEncoder


class RailFenceCipher(metaclass=TextEncoder):
    def __init__(self, key: int = 3):
        self.KEY = key
        self.rf_arr = None

        if self.KEY < 2:
            raise ValueError("The key in Rail Fence Cipher cannot be less than 2")

    def encode(self, text: str) -> str:
        self.rf_arr = np.zeros((self.KEY, len(text)), dtype='str')
        enc_text = ''

        self.__zig_zag(mode='fill', text=text)

        for i in range(len(self.rf_arr)):
            for j in range(len(self.rf_arr[0])):
                enc_text += self.rf_arr[i][j]

        return enc_text

    def decode(self, text: str) -> str:
        self.rf_arr = np.zeros((self.KEY, len(text)), dtype='str')
        text_index = 0

        self.__zig_zag(mode='fill', text='*' * len(text))

        for i in range(len(self.rf_arr)):
            for j in range(len(self.rf_arr[0])):
                if self.rf_arr[i][j] == '*':
                    self.rf_arr[i][j] = text[text_index]
                    text_index += 1

        dec_text = self.__zig_zag(mode='get')

        return dec_text

    def __zig_zag(self, mode: str, text: str = ''):
        i = j = 0
        i_increasing = True

        while True:
            if i == self.KEY - 1:
                i_increasing = False
            elif i == 0:
                i_increasing = True

            match mode:
                case 'fill':
                    if j >= len(text):
                        break
                    self.rf_arr[i][j] = text[j]
                case 'get':
                    text += self.rf_arr[i][j]
                case _:
                    raise ValueError("Mode cannot be anything other than 'fill' or 'get'.")

            if i_increasing:
                i += 1
            else:
                i -= 1
            j += 1

            if i >= len(self.rf_arr) or j >= len(self.rf_arr[0]):
                break

        if text:
            return text


class ColumnarTranspositionCipher(metaclass=TextEncoder):
    def __init__(self, key: str, filler: str = '_'):
        if self.__is_unique(key.upper()):
            self.KEY = key.upper()
            self.FILLER = filler
        else:
            raise ValueError("The key for Columnar Transposition Cipher needs to be unique")

        self.txt_arr = None
        self.ORDER_LIST = self.__get_order_list(self.KEY)

    def encode(self, text: str) -> str:
        if self.FILLER in text:
            warnings.warn(f"Filler '{self.FILLER}' is present in the text which might lead to unwanted issues.")

        self.txt_arr = np.zeros((math.ceil(len(text)/len(self.KEY)), len(self.KEY)), dtype='str')
        text_index = 0
        enc_text = ''

        for i in range(len(self.txt_arr)):
            for j in range(len(self.txt_arr[0])):
                if text_index < len(text):
                    self.txt_arr[i][j] = text[text_index]
                else:
                    self.txt_arr[i][j] = self.FILLER
                text_index += 1

        for i in range(len(self.ORDER_LIST)):
            for j in range(len(self.ORDER_LIST)):
                if self.ORDER_LIST[j] == i:
                    enc_text += ''.join(list(self.txt_arr[:, j].flatten()))

        return enc_text

    def decode(self, text: str) -> str:
        rows = len(text)//len(self.KEY)
        self.txt_arr = np.zeros((rows, len(self.KEY)), dtype='str')

        for i in range(len(self.ORDER_LIST)):
            for j in range(rows):
                self.txt_arr[j][i] = text[self.ORDER_LIST[i] * rows + j]

        dec_text = ''.join(self.txt_arr.flatten()).rstrip(self.FILLER)

        return dec_text

    def __is_unique(self, text) -> bool:
        for i in range(len(text) - 1):
            if text[i] in text[i+1:]:
                return False
        return True

    def __get_order_list(self, text: str) -> list:
        lst = [ord(i) for i in text]
        order = 0
        for i in range(65, 91):
            for j in range(len(lst)):
                if lst[j] == i:
                    lst[j] = order
                    order += 1

        return lst
