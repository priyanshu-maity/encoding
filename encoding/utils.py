"""
utils.py

This module provides utility classes for text encoding and decoding operations.

Classes:
    TextEncoder -- A metaclass ensuring encoders implement 'encode' and 'decode' methods.
    Pipeline -- A class for combining multiple encoders in sequence.
    Salt -- A class for adding and removing salt from text to enhance security.
    TextFileEncoder -- A class for encoding and decoding text files using a specified encoder.
"""

import inspect
import random
import json
import csv

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
    def __init__(self, position: str = 'between', random_seed: int = 42, min_length: int = 2, max_length: int = 7):
        random.seed(random_seed)
        self.random_state = random.getstate()
        self.characters = [chr(i) for i in range(33, 127) if chr(i) not in ['-', '\'', '\"']]
        self.min_length = min_length
        self.max_length = max_length
        self.positions = ['front', 'end', 'between']

        if position in self.positions:
            self.position = position
        else:
            raise ValueError(f"Salt position cannot be '{position}'. Valid salt positons: {', '.join(self.positions)}")

    def encode(self, text: str) -> str:
        random.setstate(self.random_state)
        match self.position:
            case 'front':
                return self.__get_salt() + text

            case 'end':
                return text + self.__get_salt()

            case 'between':
                salts = []
                for i in range(len(text)):
                    salts.append(self.__get_salt())
                return ''.join([text[i] + salts[i] for i in range(len(salts))])

    def decode(self, text: str) -> str:
        random.setstate(self.random_state)
        match self.position:
            case 'front':
                return text.removeprefix(self.__get_salt())

            case 'end':
                return text.removesuffix(self.__get_salt())

            case 'between':
                pure_text = ''
                try:
                    i = 0
                    while True:
                        pure_text += text[i]
                        i += len(self.__get_salt()) + 1
                except IndexError:
                    return pure_text

    def __get_salt(self) -> str:
        return ''.join(random.choices(self.characters, k=random.randint(self.min_length, self.max_length)))


class StructuredDataEncoder:
    def __init__(self, encoder: object):
        self.encoder = encoder

    def encode(self, data: object) -> object:
        if isinstance(data, list):
            return self.__list_encoder(data, mode='encode')
        elif isinstance(data, tuple):
            return self.__tuple_encoder(data, mode='encode')
        elif isinstance(data, dict):
            return self.__dict_encoder(data, mode='encode')
        elif isinstance(data, set):
            return self.__set_encoder(data, mode='encode')
        elif isinstance(data, frozenset):
            return self.__frozen_set_encoder(data, mode='encode')
        else:
            return self.encoder.encode(self.__get_str(data))

    def decode(self, data: object) -> object:
        if isinstance(data, list):
            return self.__list_encoder(data, mode='decode')
        elif isinstance(data, tuple):
            return self.__tuple_encoder(data, mode='decode')
        elif isinstance(data, dict):
            return self.__dict_encoder(data, mode='decode')
        elif isinstance(data, set):
            return self.__set_encoder(data, mode='decode')
        elif isinstance(data, frozenset):
            return self.__frozen_set_encoder(data, mode='decode')
        elif isinstance(data, str):
            return eval(self.encoder.decode(data))
        else:
            raise ValueError(f"Data type '{data}' is not supported.")

    def __list_encoder(self, data: list, mode: str = 'encode') -> list:
        new_list = []
        for index, datum in enumerate(data):
            if mode == 'encode':
                new_list.append(self.encode(datum))
            else:
                new_list.append(self.decode(datum))

        return new_list

    def __tuple_encoder(self, data: tuple, mode: str = 'encode') -> tuple:
        return tuple(self.__list_encoder(list(data), mode=mode))

    def __dict_encoder(self, data: dict, mode: str = 'encode') -> dict:
        new_dict = {}
        for key, value in data.items():
            if mode == 'encode':
                new_dict[self.encode(key)] = self.encode(value)
            else:
                new_dict[self.decode(key)] = self.decode(value)

        return new_dict

    def __set_encoder(self, data: set, mode: str = 'encode') -> set:
        new_set = set({})
        for element in data:
            if mode == 'encode':
                new_set.add(self.encode(element))
            else:
                new_set.add(self.decode(element))

        return new_set

    def __frozen_set_encoder(self, data: frozenset, mode: str = 'encode') -> frozenset:
        return frozenset(self.__set_encoder(set(data), mode=mode))

    def __get_str(self, obj: object) -> str:
        if isinstance(obj, (int, float, complex, bool, type(None), range, bytes, bytearray)):
            return str(obj)
        elif isinstance(obj, str):
            return f'str(\'{obj}\')'
        else:
            raise ValueError(f"Data type '{obj}' is not supported.")


class TextFileEncoder:
    def __init__(self, encoder: object):
        self.encoder = encoder

    def encode(self, file: str, file_out: str = None) -> None:
        if file[file.rindex('.') + 1:] != 'txt' or (file_out[file_out.rindex('.') + 1:] != 'txt' if file_out else False):
            raise ValueError("TextFileEncoder only supports text files with extension: '.txt'")

        enc_text = ''
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                enc_text += self.encoder.encode(line) + '\n'

        with open(file_out if file_out else file, 'w') as f:
            f.write(enc_text)

    def decode(self, file: str, file_out: str = None) -> None:
        if file[file.rindex('.') + 1:] != 'txt' or (file_out[file_out.rindex('.') + 1:] != 'txt' if file_out else False):
            raise ValueError("TextFileEncoder only supports text files with extension: '.txt'")

        dec_text = ''
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                dec_text += self.encoder.decode(line) + '\n'

        with open(file_out if file_out else file, 'w') as f:
            f.write(dec_text)


class JSONFileEncoder:
    def __init__(self, encoder: object):
        self.encoder = StructuredDataEncoder(encoder=encoder)

    def encode(self, file: str, file_out: str = None, indent: int = 4) -> None:
        if file[file.rindex('.') + 1:] != 'json' or (file_out[file_out.rindex('.') + 1:] != 'json' if file_out else False):
            raise ValueError("TextFileEncoder only supports text files with extension: '.json'")

        data = json.load(open(file, 'r'))
        enc_data = self.encoder.encode(data)

        with open(file_out if file_out else file, 'w') as f:
            json.dump(enc_data, f, indent=indent)

    def decode(self, file: str, file_out: str = None, indent: int = 4) -> None:
        if file[file.rindex('.') + 1:] != 'json' or (file_out[file_out.rindex('.') + 1:] != 'json' if file_out else False):
            raise ValueError("TextFileEncoder only supports text files with extension: '.json'")

        data = json.load(open(file, 'r'))
        dec_data = self.encoder.decode(data)

        with open(file_out if file_out else file, 'w') as f:
            json.dump(dec_data, f, indent=indent)
