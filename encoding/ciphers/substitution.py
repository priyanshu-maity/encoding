"""
substitution.py

This module provides classes for implementing various substitution ciphers, including Caesar, Atbash, Affine, and Vigenere
Ciphers. These classes use the `TextEncoder` metaclass to enforce the implementation of encoding and decoding methods.

Classes:
    CaesarCipher: Implements the Caesar Cipher for encoding and decoding text.
    AtbashCipher: Implements the Atbash Cipher for encoding and decoding text.
    AffineCipher: Implements the Affine Cipher for encoding and decoding text.
    VigenereCipher: Implements the Vigenere Cipher for encoding and decoding text.

"""

from encoding.utils import TextEncoder
import numpy as np


class CaesarCipher(metaclass=TextEncoder):
    """
    Implements the Caesar Cipher for encoding and decoding text.

    Attributes:
        shift (int): The number of positions to shift each character.
        alpha_only (bool): Whether to encode only alphabetic characters.

    Methods:
        encode(text): Encodes the given text using the Caesar Cipher.
        decode(text): Decodes the given text using the Caesar Cipher.
    """

    def __init__(self, shift: int = 3, alpha_only: bool = False):
        """
        Initializes the CaesarCipher with the specified shift and mode.

        Args:
            shift (int): The number of positions to shift each character. Default is 3.
            alpha_only (bool): Whether to encode only alphabetic characters. Default is False.
        """
        self.shift = shift
        self.alpha_only = alpha_only

    def encode(self, text: str) -> str:
        """
        Encodes the given text using the Caesar Cipher.

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
        enc_text = ""

        for i in text:
            ascii_val = ord(i)
            if self.alpha_only:
                char_value = ascii_val + self.shift
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(char_value) if char_value <= 90 else chr(char_value - 26)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(char_value) if char_value <= 122 else chr(char_value - 26)
                else:
                    rep_letter = i
            else:
                rep_letter = chr(((ascii_val - 32 + self.shift) % 95) + 32)
            enc_text += rep_letter

        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the given text using the Caesar Cipher.

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

        dec_text = ""
        for i in text:
            ascii_val = ord(i)
            if self.alpha_only:
                char_val = ascii_val - self.shift
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(char_val) if char_val >= 65 else chr(char_val + 26)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(char_val) if char_val >= 97 else chr(char_val + 26)
                else:
                    rep_letter = i
            else:
                rep_letter = chr(((ascii_val - 32 - self.shift) % 95) + 32)
            dec_text += rep_letter

        return dec_text


class AtbashCipher(metaclass=TextEncoder):
    """
    Implements the Atbash Cipher for encoding and decoding text.

    Attributes:
        alpha_only (bool): Whether to encode only alphabetic characters.

    Methods:
        encode(text): Encodes the given text using the Atbash Cipher.
        decode(text): Decodes the given text using the Atbash Cipher.
    """

    def __init__(self, alpha_only: bool = False):
        """
        Initializes the AtbashCipher with the specified mode.

        Args:
            alpha_only (bool): Whether to encode only alphabetic characters. Default is False.
        """
        self.alpha_only = alpha_only

    def encode(self, text: str) -> str:
        """
        Encodes the given text using the Atbash Cipher.

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

        enc_text = ""

        for i in text:
            ascii_val = ord(i)
            if self.alpha_only:
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(155 - ascii_val)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(219 - ascii_val)
                else:
                    rep_letter = i
            else:
                rep_letter = chr(126 - (ascii_val - 32))
            enc_text += rep_letter

        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the given text using the Atbash Cipher.

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

        return self.encode(text=text)


class AffineCipher(metaclass=TextEncoder):
    """
    Implements the Affine Cipher for encoding and decoding text.

    Attributes:
        key_a (int): The multiplicative key.
        key_b (int): The additive key.
        alpha_only (bool): Whether to encode only alphabetic characters.

    Methods:
        encode(text): Encodes the given text using the Affine Cipher.
        decode(text): Decodes the given text using the Affine Cipher.
    """

    def __init__(self, key_a: int = 3, key_b: int = 3, alpha_only: bool = False):
        """
        Initializes the AffineCipher with the specified keys and mode.

        Args:
            key_a (int): The multiplicative key. Default is 3.
            key_b (int): The additive key. Default is 3.
            alpha_only (bool): Whether to encode only alphabetic characters. Default is False.

        Raises:
            ValueError: If the keys are out of the valid range or not coprime with the modulus.
        """
        self.key_a = key_a
        self.key_b = key_b
        self.alpha_only = alpha_only

        if not 0 <= self.key_a <= 26 and self.alpha_only:
            raise ValueError(
                f"'key_a' cannot have a value {self.key_a}. Value must be within the range: 0 <= 'key_a' <= 26.")

        if not 0 <= self.key_a <= 127 and not self.alpha_only:
            raise ValueError(
                f"'key_a' cannot have a value {self.key_a}. Value must be within the range: 0 <= 'key_a' <= 127.")

        if not self.__coprime():
            raise ValueError(f"'key_a' cannot have a value {self.key_a}. Value must be coprime with",
                             "26" if self.alpha_only else "128")

    def encode(self, text: str) -> str:
        """
        Encodes the given text using the Affine Cipher.

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

        enc_text = ""

        for i in text:
            ascii_val = ord(i)
            if 65 <= ascii_val <= 90:
                x = ascii_val - 65 if self.alpha_only else ascii_val
            elif 97 <= ascii_val <= 122:
                x = ascii_val - 97 if self.alpha_only else ascii_val
            else:
                if self.alpha_only:
                    enc_text += i
                    continue
                else:
                    x = ascii_val
            m = 26 if self.alpha_only else 95
            rep_letter = chr(((self.key_a * (x - (0 if self.alpha_only else 32)) + self.key_b) % m) + (65 if self.alpha_only else 32))
            if self.alpha_only:
                rep_letter = rep_letter.lower() if chr(ascii_val).islower() else rep_letter.upper()
            enc_text += rep_letter

        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the given text using the Affine Cipher.

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
        dec_text = ""

        for i in text:
            ascii_val = ord(i)
            if 65 <= ascii_val <= 90:
                x = ascii_val - 65 if self.alpha_only else ascii_val
            elif 97 <= ascii_val <= 122:
                x = ascii_val - 97 if self.alpha_only else ascii_val
            else:
                if self.alpha_only:
                    dec_text += i
                    continue
                else:
                    x = ascii_val

            m = 26 if self.alpha_only else 95
            key_inv = self.__mod_inverse(m)
            if not key_inv:
                raise ValueError("Unexpected error occurred.")
            rep_letter = chr((key_inv * (x - (0 if self.alpha_only else 32) - self.key_b) % m) + (0 if self.alpha_only else 32))
            if self.alpha_only:
                rep_letter = chr((ord(rep_letter) + 65) if chr(ascii_val).isupper() else (ord(rep_letter) + 97))
            dec_text += rep_letter

        return dec_text

    def __mod_inverse(self, m):
        """
        Computes the modular inverse of key_a with respect to the modulus m.

        Args:
            m (int): The modulus.

        Returns:
            int: The modular inverse of key_a.
        """
        for i in range(1, m):
            if (self.key_a * i) % m == 1:
                return i
        return None

    def __coprime(self) -> bool:
        """
        Checks if key_a is coprime with the modulus.

        Returns:
            bool: True if key_a is coprime with the modulus, False otherwise.
        """
        a = self.key_a
        b = 26 if self.alpha_only else 95
        while b != 0:
            a, b = b, a % b
        return a == 1


class VigenereCipher(metaclass=TextEncoder):
    """
    Implements the Vigenere Cipher for encoding and decoding text.

    Attributes:
        key (str): The key to use for the cipher.
        alpha_only (bool): Whether to encode only alphabetic characters.
        final_key (str): The repeated key to match the length of the text.

    Methods:
        encode(text): Encodes the given text using the Vigenere Cipher.
        decode(text): Decodes the given text using the Vigenere Cipher.
    """

    def __init__(self, key: str = 'KEY', alpha_only: bool = False):
        """
        Initializes the VigenereCipher with the specified key and mode.

        Args:
            key (str): The key to use for the cipher. Default is 'KEY'.
            alpha_only (bool): Whether to encode only alphabetic characters. Default is False.

        Raises:
            ValueError: If the key is empty.
        """
        self.key = key
        self.alpha_only = alpha_only
        self.final_key = ""

        if self.key == "":
            raise ValueError("Key value cannot be null")

    def encode(self, text: str) -> str:
        """
        Encodes the given text using the Vigenere Cipher.

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

        self.final_key = (self.key * (len(text) // len(self.key) + 1)).upper()
        enc_text = ""
        if self.alpha_only:
            matrix = self.__generate_matrix()

        for i in range(len(text)):
            if self.alpha_only:
                if self.final_key[i].isalpha():
                    if 65 <= ord(text[i]) <= 90:
                        rep_letter = matrix[ord(text[i]) - 65][ord(self.final_key[i].upper()) - 65]
                    elif 97 <= ord(text[i]) <= 122:
                        rep_letter = matrix[ord(text[i]) - 97][ord(self.final_key[i].lower()) - 97]
                        rep_letter = rep_letter.lower()
                    else:
                        rep_letter = text[i]
                else:
                    raise ValueError("Key must be composed of alphabets in Alphabet Only mode")
            else:
                rep_letter = chr((((ord(text[i]) - 32) + (ord(self.final_key[i]) - 32)) % 95) + 32)
            enc_text += rep_letter
        return enc_text

    def decode(self, text: str) -> str:
        """
        Decodes the given text using the Vigenere Cipher.

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

        self.final_key = (self.key * (len(text) // len(self.key) + 1)).upper()
        dec_text = ""
        if self.alpha_only:
            matrix = self.__generate_matrix()

        for i in range(len(text)):
            if self.alpha_only:
                index = np.where(matrix[0] == self.final_key[i])
                letter = text[i].upper() if self.alpha_only else text[i]

                if not self.final_key[i].isalpha():
                    raise ValueError("Key must be composed of alphabets in Alphabet Only mode")

                for j in range(len(matrix)):
                    if matrix[j][index] == letter:
                        break

                if 65 <= ord(text[i]) <= 90:
                    rep_letter = matrix[j][0]
                elif 97 <= ord(text[i]) <= 122:
                    rep_letter = matrix[j][0]
                    rep_letter = rep_letter.lower()
                else:
                    rep_letter = text[i]
            else:
                rep_letter = chr((((ord(text[i]) - 32) - (ord(self.final_key[i]) - 32)) % 95) + 32)

            dec_text += rep_letter
        return dec_text

    def __generate_matrix(self):
        """
        Generates the Vigenere matrix for alphabetic encoding.

        Returns:
            ndarray: The Vigenere matrix.
        """
        elements = np.array([chr(i) for i in range(65, 91)], dtype='<U1')
        matrix = np.empty((26, 26), dtype='<U1')

        for i in range(len(elements)):
            matrix[i] = np.roll(elements, -i)

        return matrix
