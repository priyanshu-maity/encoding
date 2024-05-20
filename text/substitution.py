from encoding import TextEncoder


class CaesarCipher(metaclass=TextEncoder):
    def __init__(self, key: int = 2):
        self.KEY = key
        self.__is_key_default = True

    def encode(self, text: str) -> str:
        enc_text = ""

        for i in range(len(text)):
            rep_letter = (ord(text[i]) + self.KEY) % 149187
            enc_text += chr(rep_letter)

        if not self.__is_key_default:
            self.__is_key_default = not self.__is_key_default
            self.KEY *= -1

        return enc_text

    def decode(self, text: str) -> str:
        self.KEY *= -1
        self.__is_key_default = not self.__is_key_default
        return self.encode(text=text)
