"""
text.transposition.py

This module provides transposition cipher classes for text encoding and decoding operations.

Classes:
    RailFenceCipher -- A class for encoding and decoding text using the Rail Fence Cipher technique.
    ColumnarTranspositionCipher -- A class for encoding and decoding text using the Columnar Transposition Cipher technique.
"""

import numpy as np
import math
import warnings

from utils import TextEncoder


class RailFenceCipher(metaclass=TextEncoder):
    """
    RailFenceCipher class for encoding and decoding text using the Rail Fence Cipher technique.

    Attributes:
        key (int): The key for the number of rails in the Rail Fence Cipher (default: 3).

    Methods:
        __init__(self, key: int = 3):
            Initializes the RailFenceCipher object with the specified key.
        encode(self, text: str) -> str:
            Encodes the input text using the Rail Fence Cipher.
        decode(self, text: str) -> str:
            Decodes the input text using the Rail Fence Cipher.

    Private Methods:
        __zig_zag(self, mode: str, text: str = ''):
            Implements the zig-zag pattern for encoding and decoding.
    """

    def __init__(self, key: int = 3):
        """
        Initializes the RailFenceCipher object with the specified key.

        Parameters:
            key (int, optional): The key for the number of rails in the Rail Fence Cipher (default: 3).

        Raises:
            ValueError: If the key is less than 2.
        """

        self.key = key
        self.rf_arr = None

        if self.key < 2:
            raise ValueError("The key in Rail Fence Cipher cannot be less than 2")

    def encode(self, text: str) -> str:
        """
        Encodes the input text using the Rail Fence Cipher.

        Parameters:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.

        Raises:
            ValueError: If any character in the input text has ASCII value greater than 127.
        """

        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")
        self.rf_arr = np.zeros((self.key, len(text)), dtype='str')
        enc_text = ''

        self.__zig_zag(mode='fill', text=text)

        for i in range(len(self.rf_arr)):
            for j in range(len(self.rf_arr[0])):
                enc_text += self.rf_arr[i][j]

        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the input text using the Rail Fence Cipher.

        Parameters:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.

        Raises:
            ValueError: If any character in the input text has ASCII value greater than 127.
        """

        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")

        self.rf_arr = np.zeros((self.key, len(text)), dtype='str')
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
        """
        Implements the zig-zag pattern for encoding and decoding.

        Parameters:
            mode (str): The mode of operation ('fill' or 'get').
            text (str, optional): The text to be processed (default is '').

        Returns:
            str: The processed text if mode is 'get', else None.

        Raises:
            ValueError: If mode is neither 'fill' nor 'get'.
        """

        i = j = 0
        i_increasing = True

        while True:
            if i == self.key - 1:
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
    """
    ColumnarTranspositionCipher class for encoding and decoding text using the Columnar Transposition Cipher technique.

    Attributes:
        key (str): The key for the Columnar Transposition Cipher (default: 'key').
        filler (str): The filler character used for padding (default: '_').

    Methods:
        __init__(self, key: str = 'key', filler: str = '_'):
            Initializes the ColumnarTranspositionCipher object with the specified key and filler.
        encode(self, text: str) -> str:
            Encodes the input text using the Columnar Transposition Cipher.
        decode(self, text: str) -> str:
            Decodes the input text using the Columnar Transposition Cipher.

    Private Methods:
        __is_unique(self, text) -> bool:
            Checks if all characters in the input text are unique.
        __get_order_list(self, text: str) -> list:
            Generates an order list based on the characters in the input text.
    """

    def __init__(self, key: str = "key", filler: str = "_"):
        """
        Initializes the ColumnarTranspositionCipher object with the specified key and filler.

        Parameters:
            key (str, optional): The key for the Columnar Transposition Cipher (default: 'key').
            filler (str, optional): The filler character used for padding (default: '_').

        Raises:
            ValueError: If the key is not unique.
        """

        if self.__is_unique(key.upper()):
            self.key = key.upper()
            self.filler = filler
        else:
            raise ValueError("The key for Columnar Transposition Cipher needs to be unique")

        self.txt_arr = None
        self.order_list = self.__get_order_list(self.key)

    def encode(self, text: str) -> str:
        """
        Encodes the input text using the Columnar Transposition Cipher.

        Parameters:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.

        Raises:
            ValueError: If any character in the input text has ASCII value greater than 127.
            Warning: If the filler character is present in the input text.
        """

        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")

        if self.filler in text:
            warnings.warn(f"Filler '{self.filler}' is present in the text which might lead to unwanted issues.")

        self.txt_arr = np.zeros((math.ceil(len(text)/len(self.key)), len(self.key)), dtype='str')
        text_index = 0
        enc_text = ''

        for i in range(len(self.txt_arr)):
            for j in range(len(self.txt_arr[0])):
                if text_index < len(text):
                    self.txt_arr[i][j] = text[text_index]
                else:
                    self.txt_arr[i][j] = self.filler
                text_index += 1

        for i in range(len(self.order_list)):
            for j in range(len(self.order_list)):
                if self.order_list[j] == i:
                    enc_text += ''.join(list(self.txt_arr[:, j].flatten()))

        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the input text using the Columnar Transposition Cipher.

        Parameters:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.

        Raises:
            ValueError: If any character in the input text has ASCII value greater than 127.
        """

        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")

        rows = len(text)//len(self.key)
        self.txt_arr = np.zeros((rows, len(self.key)), dtype='str')

        for i in range(len(self.order_list)):
            for j in range(rows):
                self.txt_arr[j][i] = text[self.order_list[i] * rows + j]

        dec_text = ''.join(self.txt_arr.flatten()).rstrip(self.filler)

        return dec_text

    def __is_unique(self, text) -> bool:
        """
        Checks if all characters in the input text are unique.

        Parameters:
            text (str): The text to be checked.

        Returns:
            bool: True if all characters are unique, False otherwise.
        """

        for i in range(len(text) - 1):
            if text[i] in text[i+1:]:
                return False
        return True

    def __get_order_list(self, text: str) -> list:
        """
        Generates an order list based on the characters in the input text.

        Parameters:
            text (str): The text to generate the order list from.

        Returns:
            list: The order list.
        """

        lst = [ord(i) for i in text]
        order = 0
        for i in range(65, 91):
            for j in range(len(lst)):
                if lst[j] == i:
                    lst[j] = order
                    order += 1

        return lst
