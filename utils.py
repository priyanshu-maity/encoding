import inspect
import random

from tqdm import tqdm


class TextEncoder(type):
    def __new__(cls, name, bases, dct):
        if 'encode' not in dct or 'decode' not in dct:
            raise TypeError(f"Class {name} must implement both encode and decode methods")

        if not callable(dct['encode']) or not callable(dct['decode']):
            raise TypeError(f"Both encode and decode must be callable")

        check_methods = ['encode', 'decode']
        for method in check_methods:
            signature = inspect.signature(dct[method])
            expected_params = ['self', 'text']
            params = list(signature.parameters.keys())
            if expected_params != params or signature.return_annotation != str:
                raise TypeError(f"Method '{method}' must take 'self' and 'text' parameters and return a string")

        return super().__new__(cls, name, bases, dct)


class Pipeline:
    def __init__(self, encoders: list):
        self.encoder_names = []

        if self.__is_valid(encoders):
            self.encoders = encoders
            self.__get_encoder_names()
        else:
            raise ValueError("Encoders must be passed as a tuple of class object and names of the encoders.")

    def encode(self, text: str) -> str:
        for encoder in self.encoders:
            text = encoder[0].encode(text)

        return text

    def decode(self, text: str) -> str:
        for decoder in self.encoders[::-1]:
            text = decoder[0].decode(text)

        return text

    def add_encoders(self, encoders: list):
        if self.__is_valid(encoders):
            self.encoders.extend(encoders)
            self.__get_encoder_names()
        else:
            raise ValueError("Encoders must be passed as tuples of class object and names of the encoders.")

    def remove_encoders(self, encoder_names: list):
        for encoder_name in encoder_names:
            if type(encoder_name) != str:
                raise ValueError("Encoders must be passed as a list of encoder names.")
            if encoder_name not in self.encoder_names:
                raise ValueError("Encoder names given are unavailable in original list of encoders.")

        temp_encoders = []
        for encoder in self.encoders:
            if encoder[1] not in encoder_names:
                temp_encoders.append(encoder)

        self.encoders = temp_encoders
        self.__get_encoder_names()

    def __is_valid(self, encoders) -> bool:
        for encoder in encoders:
            if len(encoder) != 2:
                return False

            if type(encoder[1]) != str:
                return False

        return True

    def __get_encoder_names(self):
        self.encoder_names.clear()
        for encoder in self.encoders:
            if encoder in self.encoder_names:
                raise ValueError(f"Two encoders cannot have the same name: {encoder}.")
            self.encoder_names.append(encoder[1])


class Salt:
    def __init__(self, position: str = 'all', random_seed: int = 42, min_length: int = 2, max_length: int = 7):
        random.seed(random_seed)
        self.RANDOM_STATE = random.getstate()
        self.CHARACTERS = [chr(i) for i in range(33, 127)]
        self.MIN_LENGTH = min_length
        self.MAX_LENGTH = max_length
        self.POSITIONS = ['front', 'end', 'all']

        if position in self.POSITIONS:
            self.POSITION = position
        else:
            raise ValueError(f"Salt position cannot be '{position}'. Valid salt positons: {', '.join(self.POSITIONS)}")

    def encode(self, text: str) -> str:
        random.setstate(self.RANDOM_STATE)
        match self.POSITION:
            case 'front':
                return self.__get_salt() + text

            case 'end':
                return text + self.__get_salt()

            case 'all':
                salts = []
                for i in range(len(text)):
                    salts.append(self.__get_salt())
                return ''.join([text[i] + salts[i] for i in range(len(salts))])

    def decode(self, text: str) -> str:
        random.setstate(self.RANDOM_STATE)
        match self.POSITION:
            case 'front':
                return text.removeprefix(self.__get_salt())

            case 'end':
                return text.removesuffix(self.__get_salt())

            case 'all':
                pure_text = ''
                try:
                    i = 0
                    while True:
                        pure_text += text[i]
                        i += len(self.__get_salt()) + 1
                except IndexError:
                    return pure_text

    def __get_salt(self) -> str:
        return ''.join(random.choices(self.CHARACTERS, k=random.randint(self.MIN_LENGTH, self.MAX_LENGTH)))


class FileEncoder:
    def __init__(self, encoder: object):
        self.encoder = encoder

    def encode(self, file: str, file_out: str = None, progressbar: bool = True) -> None:
        enc_text = ''

        with open(file, 'r') as f:
            if progressbar:
                bar = tqdm(desc="Encoding", total=len(f.readlines()), unit=" lines")
                f.seek(0)

            for line in f:
                line = line.strip()
                enc_text += self.encoder.encode(line) + '\n'
                if progressbar:
                    bar.update(1)

            if progressbar:
                bar.close()

        with open(file_out if file_out else file, 'w') as f:
            f.write(enc_text)

    def decode(self, file: str, file_out: str = None, progressbar: bool = True) -> None:
        dec_text = ''

        with open(file, 'r') as f:
            if progressbar:
                bar = tqdm(desc="Decoding", total=len(f.readlines()), unit=" lines")
                f.seek(0)

            for line in f:
                line = line.strip()
                dec_text += self.encoder.decode(line) + '\n'
                if progressbar:
                    bar.update(1)

            if progressbar:
                bar.close()

        with open(file_out if file_out else file, 'w') as f:
            f.write(dec_text)
