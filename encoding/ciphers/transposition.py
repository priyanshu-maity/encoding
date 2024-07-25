"""
transposition.py

This module provides classes for implementing transposition ciphers, specifically the Rail Fence Cipher and the Columnar
Transposition Cipher. These classes use the `TextEncoder` metaclass to enforce the implementation of encoding and decoding
methods.

Classes:
    RailFenceCipher: Implements the Rail Fence Cipher for encoding and decoding text.
    ColumnarTranspositionCipher: Implements the Columnar Transposition Cipher for encoding and decoding text.

"""

import numpy as np
import math
import warnings

from encoding.utils import TextEncoder


class RailFenceCipher(metaclass=TextEncoder):
    """
    Implements the Rail Fence Cipher for encoding and decoding text.

    Attributes:
        rails (int): The number of rails to use in the cipher.
        rf_arr (ndarray): The array used to store the zig-zag pattern of characters.

    Methods:
        encode(text): Encodes the given text using the Rail Fence Cipher.
        decode(text): Decodes the given text using the Rail Fence Cipher.
    """

    def __init__(self, rails: int = 3):
        """
        Initializes the RailFenceCipher with the specified number of rails.

        Args:
            rails (int): The number of rails to use in the cipher. Default is 3.

        Raises:
            ValueError: If the number of rails is less than 2.
        """
        self.rails = rails
        self.rf_arr = None

        if self.rails < 2:
            raise ValueError("The key in Rail Fence Cipher cannot be less than 2")

    def encode(self, text: str) -> str:
        """
        Encodes the given text using the Rail Fence Cipher.

        Args:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.

        Raises:
            ValueError: If the text contains characters with ASCII < 32 or ASCII > 127.
        """
        if not text:
            return text

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")
        self.rf_arr = np.zeros((self.rails, len(text)), dtype='<U1')
        enc_text = ''

        self.__zig_zag(mode='fill', text=text)

        for i in range(len(self.rf_arr)):
            for j in range(len(self.rf_arr[0])):
                enc_text += self.rf_arr[i][j]

        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the given text using the Rail Fence Cipher.

        Args:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.

        Raises:
            ValueError: If the text contains characters with ASCII < 32 or ASCII > 127.
        """
        if not text:
            return text

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        self.rf_arr = np.zeros((self.rails, len(text)), dtype='<U1')
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
        Helper method to fill the zig-zag pattern in the rail fence array.

        Args:
            mode (str): The mode of operation ('fill' or 'get').
            text (str): The text to fill in the zig-zag pattern.

        Returns:
            str: The text obtained from the zig-zag pattern if mode is 'get'.

        Raises:
            ValueError: If the mode is not 'fill' or 'get'.
        """
        i = j = 0
        i_increasing = True

        while True:
            if i == self.rails - 1:
                i_increasing = False
            elif i == 0:
                i_increasing = True

            if mode == 'fill':
                if j >= len(text):
                    break
                self.rf_arr[i][j] = text[j]
            elif mode == 'get':
                text += self.rf_arr[i][j]
            else:
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
    Implements the Columnar Transposition Cipher for encoding and decoding text.

    Attributes:
        key (str): The key to use for the cipher.
        filler (str): The filler character to use for padding.
        txt_arr (ndarray): The array used to store the characters in columnar order.
        order_list (list): The order of columns based on the key.

    Methods:
        encode(text): Encodes the given text using the Columnar Transposition Cipher.
        decode(text): Decodes the given text using the Columnar Transposition Cipher.
    """

    def __init__(self, key: str = "key", filler: str = "_"):
        """
        Initializes the ColumnarTranspositionCipher with the specified key and filler.

        Args:
            key (str): The key to use for the cipher. Default is "key".
            filler (str): The filler character to use for padding. Default is "_".

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
        Encodes the given text using the Columnar Transposition Cipher.

        Args:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.

        Raises:
            ValueError: If the text contains characters with ASCII < 32 or ASCII > 127.
            warnings.warn: If the filler character is present in the text.
        """
        if not text:
            return text

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        if self.filler in text:
            warnings.warn(f"Filler '{self.filler}' is present in the text which might lead to unwanted issues.")

        self.txt_arr = np.zeros((math.ceil(len(text)/len(self.key)), len(self.key)), dtype='<U1')
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
        Decodes the given text using the Columnar Transposition Cipher.

        Args:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.

        Raises:
            ValueError: If the text contains characters with ASCII < 32 or ASCII > 127.
        """
        if not text:
            return text

        if not any(32 <= ord(char) <= 126 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII < 32 or ASCII > 127")

        rows = len(text)//len(self.key)
        self.txt_arr = np.zeros((rows, len(self.key)), dtype='<U1')

        for i in range(len(self.order_list)):
            for j in range(rows):
                self.txt_arr[j][i] = text[self.order_list[i] * rows + j]

        dec_text = ''.join(self.txt_arr.flatten()).rstrip(self.filler)

        return dec_text

    def __is_unique(self, text) -> bool:
        """
        Checks if all characters in the given text are unique.

        Args:
            text (str): The text to check.

        Returns:
            bool: True if all characters are unique, False otherwise.
        """
        for i in range(len(text) - 1):
            if text[i] in text[i+1:]:
                return False
        return True

    def __get_order_list(self, text: str) -> list:
        """
        Generates the order list based on the key.

        Args:
            text (str): The key to generate the order list from.

        Returns:
            list: The order list based on the key.
        """
        lst = [ord(i) for i in text]
        order = 0
        for i in range(65, 91):
            for j in range(len(lst)):
                if lst[j] == i:
                    lst[j] = order
                    order += 1

        return lst
