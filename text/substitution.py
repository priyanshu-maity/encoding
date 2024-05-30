import warnings

from encoding import TextEncoder


class CaesarCipher(metaclass=TextEncoder):
    def __init__(self, key: int = 2, alpha_only: bool = False):
        self.KEY = key
        self.__is_key_default = True
        self.ALPHA_ONLY = alpha_only

        if self.ALPHA_ONLY:
            warnings.warn(
                message="Caesar Cipher is in Alphabet only mode. To change it, set 'alpha_only' to False",
                category=UserWarning
            )

    def encode(self, text: str) -> str:
        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")
        enc_text = ""

        for i in text:
            ascii_val = ord(i)

            if self.ALPHA_ONLY:
                char_value = (ascii_val + self.KEY)
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(char_value) if char_value <= 90 else chr(char_value - 26)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(char_value) if char_value <= 122 else chr(char_value - 26)
                else:
                    rep_letter = i
            else:
                rep_letter = chr((ascii_val + self.KEY) % 128)
            enc_text += rep_letter

        if not self.__is_key_default:
            self.__is_key_default = not self.__is_key_default
            self.KEY *= -1

        return enc_text

    def decode(self, text: str) -> str:
        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")
        if self.ALPHA_ONLY:
            dec_text = ""
            for i in text:
                ascii_val = ord(i)
                char_val = ascii_val - self.KEY
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(char_val) if char_val >= 65 else chr(char_val + 26)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(char_val) if char_val >= 97 else chr(char_val + 26)
                else:
                    rep_letter = i
                dec_text += rep_letter
            return dec_text
        else:
            self.KEY *= -1
            self.__is_key_default = not self.__is_key_default
            return self.encode(text=text)


class AtbashCipher(metaclass=TextEncoder):
    def __init__(self, alpha_only: bool = False):
        self.ALPHA_ONLY = alpha_only
        if self.ALPHA_ONLY:
            warnings.warn(
                message="Atbash Cipher is in Alphabet only mode. To change it, set 'alpha_only' to False",
                category=UserWarning
            )

    def encode(self, text: str) -> str:
        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")

        enc_text = ""

        for i in text:
            ascii_val = ord(i)
            if self.ALPHA_ONLY:
                if 65 <= ascii_val <= 90:
                    rep_letter = chr(155 - ascii_val)
                elif 97 <= ascii_val <= 122:
                    rep_letter = chr(219 - ascii_val)
                else:
                    rep_letter = i
            else:
                rep_letter = chr(127 - ascii_val)
            enc_text += rep_letter

        return enc_text

    def decode(self, text: str) -> str:
        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")
        return self.encode(text=text)


class AffineCipher(metaclass=TextEncoder):
    def __init__(self, key_a, key_b, alpha_only: bool = False):
        self.KEY_A = key_a
        self.KEY_B = key_b
        self.ALPHA_ONLY = alpha_only

        if type(self.KEY_A) != int:
            raise ValueError("'key_a' must be of type integer")
        if type(self.KEY_B) != int:
            raise ValueError("'key_b' must be of type integer")
        if self.ALPHA_ONLY:
            warnings.warn(
                message="Affine Cipher is in Alphabet only mode. To change it, set 'alpha_only' to False",
                category=UserWarning
            )

        if not 0 <= self.KEY_A <= 26 and self.ALPHA_ONLY:
            raise ValueError(
                f"'key_a' cannot have a value {self.KEY_A}. Value must be within the range: 0 <= 'key_a' <= 26.")

        if not 0 <= self.KEY_A <= 127 and not self.ALPHA_ONLY:
            raise ValueError(
                f"'key_a' cannot have a value {self.KEY_A}. Value must be within the range: 0 <= 'key_a' <= 127.")

        if not self.__coprime():
            raise ValueError(f"'key_a' cannot have a value {self.KEY_A}. Value must be coprime with",
                             "26" if self.ALPHA_ONLY else "128")

    def encode(self, text: str) -> str:
        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")

        enc_text = ""

        for i in text:
            ascii_val = ord(i)
            if 65 <= ascii_val <= 90:
                x = ascii_val - 65 if self.ALPHA_ONLY else ascii_val
            elif 97 <= ascii_val <= 122:
                x = ascii_val - 97 if self.ALPHA_ONLY else ascii_val
            else:
                if self.ALPHA_ONLY:
                    enc_text += i
                    continue
                else:
                    x = ascii_val
            m = 26 if self.ALPHA_ONLY else 128
            rep_letter = chr(((self.KEY_A * x + self.KEY_B) % m) + (65 if self.ALPHA_ONLY else 0))
            enc_text += rep_letter

        return enc_text

    def decode(self, text: str) -> str:
        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")
        dec_text = ""

        for i in text:
            ascii_val = ord(i)
            if 65 <= ascii_val <= 90:
                x = ascii_val - 65 if self.ALPHA_ONLY else ascii_val
            elif 97 <= ascii_val <= 122:
                x = ascii_val - 97 if self.ALPHA_ONLY else ascii_val
            else:
                if self.ALPHA_ONLY:
                    dec_text += i
                    continue
                else:
                    x = ascii_val

            m = 26 if self.ALPHA_ONLY else 128
            key_inv = self.__mod_inverse(m)
            if not key_inv:
                raise ValueError("Unexpected error occurred.")
            rep_letter = chr((key_inv * (x - self.KEY_B) % m) + (65 if self.ALPHA_ONLY else 0))
            dec_text += rep_letter

        return dec_text

    def __mod_inverse(self, m):
        for i in range(1, m):
            if (self.KEY_A * i) % m == 1:
                return i
        return None

    def __coprime(self) -> bool:
        a = self.KEY_A
        b = 26 if self.ALPHA_ONLY else 128
        while b != 0:
            a, b = b, a % b
        return a == 1


class VigenereCipher(metaclass=TextEncoder):
    def __init__(self, key: str = 'KEY', alpha_only: bool = False):
        self.KEY = key
        self.ALPHA_ONLY = alpha_only
        if self.ALPHA_ONLY:
            warnings.warn(
                message="Vigenere Cipher is in Alphabet only mode. To change it, set 'alpha_only' to False",
                category=UserWarning
            )

    def encode(self, text: str) -> str:
        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")

        final_key = (self.KEY * (len(text) // len(self.KEY) + 1)).upper()
        enc_text = ""

        for i in range(len(text)):
            if self.ALPHA_ONLY:
                if 65 <= ord(text[i]) <= 90:
                    rep_letter = chr(((ord(text[i]) + ord(final_key[i])) % 26) + 65)
                elif 97 <= ord(text[i]) <= 122:
                    rep_letter = chr(((ord(text[i].upper()) + ord(final_key[i])) % 26) + 65).lower()
                else:
                    rep_letter = text[i]
            else:
                rep_letter = chr(((ord(text[i]) + ord(final_key[i])) % 128) + 63)
            enc_text += rep_letter

        return enc_text

    def decode(self, text: str) -> str:
        if any(ord(char) > 127 for char in text):
            raise ValueError("Text Encoders cannot handle characters with ASCII > 127")

        final_key = (self.KEY * (len(text) // len(self.KEY) + 1)).upper()
        dec_text = ""

        for i in range(len(text)):
            if self.ALPHA_ONLY:
                if 65 <= ord(text[i]) <= 90:
                    rep_letter = chr(((ord(text[i]) - ord(final_key[i]) + 26) % 26) + 65)
                elif 97 <= ord(text[i]) <= 122:
                    rep_letter = chr(((ord(text[i].upper()) - ord(final_key[i]) + 26) % 26) + 65).lower()
                else:
                    rep_letter = text[i]
            else:
                rep_letter = chr(((ord(text[i]) - 63 - ord(final_key[i])) % 128))
            dec_text += rep_letter

        return dec_text
