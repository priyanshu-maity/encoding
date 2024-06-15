"""
utils.py

This module provides various classes for encoding and decoding text, structured data, and files. It includes a metaclass
to enforce method implementations, classes for text transformations, and file handlers for text and JSON files.

Classes:
    TextEncoder: A metaclass to ensure the implementation of `encode` and `decode` methods in derived classes.
    Pipeline: A class for managing a sequence of encoders and applying them to text.
    Salt: A class for adding and removing random characters (salt) to/from text.
    StructuredDataEncoder: A class for encoding and decoding structured data (lists, tuples, dicts, sets).
    TextFileEncoder: A class for encoding and decoding text files.
    JSONFileEncoder: A class for encoding and decoding JSON files.

"""

import inspect
import random
import json


class TextEncoder(type):
    """
    A metaclass that enforces the implementation of `encode` and `decode` methods in derived classes.

    The methods `encode` and `decode` must be callable, take `self` and `text` as parameters, and return a string.
    """

    def __new__(cls, name, bases, dct):
        """
        Creates a new class ensuring it has `encode` and `decode` methods.

        Args:
            cls (type): The metaclass itself.
            name (str): The name of the class being created.
            bases (tuple): The base classes of the class being created.
            dct (dict): The dictionary containing the class attributes.

        Returns:
            type: The newly created class.

        Raises:
            TypeError: If `encode` or `decode` methods are missing, not callable, or do not have the correct signature.
        """
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
    """
    A class for managing a sequence of encoders and applying them to text.

    Attributes:
        encoders (list): A list of encoder classes and their names.
        encoder_names (list): A list of encoder names.

    Methods:
        encode(text): Encodes the given text using the sequence of encoders.
        decode(text): Decodes the given text using the sequence of decoders.
        add_encoders(encoders): Adds more encoders to the sequence.
        remove_encoders(encoder_names): Removes encoders from the sequence by their names.
    """

    def __init__(self, encoders: list):
        """
        Initializes the Pipeline with a list of encoders.

        Args:
            encoders (list): A list of tuples containing encoder class objects and their names.

        Raises:
            ValueError: If the encoders are not passed as a list of tuples with class object and name.
        """
        self.encoder_names = []

        if self.__is_valid(encoders):
            self.encoders = encoders
            self.__get_encoder_names()
        else:
            raise ValueError("Encoders must be passed as a tuple of class object and names of the encoders.")

    def encode(self, text: str) -> str:
        """
        Encodes the given text using the sequence of encoders.

        Args:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.
        """
        for encoder in self.encoders:
            text = encoder[0].encode(text)

        return text

    def decode(self, text: str) -> str:
        """
        Decodes the given text using the sequence of decoders.

        Args:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.
        """
        for decoder in self.encoders[::-1]:
            text = decoder[0].decode(text)

        return text

    def add_encoders(self, encoders: list):
        """
        Adds more encoders to the sequence.

        Args:
            encoders (list): A list of tuples containing encoder class objects and their names.

        Raises:
            ValueError: If the encoders are not passed as tuples of class object and names.
        """
        if self.__is_valid(encoders):
            self.encoders.extend(encoders)
            self.__get_encoder_names()
        else:
            raise ValueError("Encoders must be passed as tuples of class object and names of the encoders.")

    def remove_encoders(self, encoder_names: list):
        """
        Removes encoders from the sequence by their names.

        Args:
            encoder_names (list): A list of encoder names to be removed.

        Raises:
            ValueError: If encoder names are not strings or are not found in the original list of encoders.
        """
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
        """
        Validates the format of encoders.

        Args:
            encoders (list): A list of tuples containing encoder class objects and their names.

        Returns:
            bool: True if valid, False otherwise.
        """
        for encoder in encoders:
            if len(encoder) != 2:
                return False

            if type(encoder[1]) != str:
                return False

        return True

    def __get_encoder_names(self):
        """
        Updates the list of encoder names.
        """
        self.encoder_names.clear()
        for encoder in self.encoders:
            if encoder in self.encoder_names:
                raise ValueError(f"Two encoders cannot have the same name: {encoder}.")
            self.encoder_names.append(encoder[1])


class Salt:
    """
    A class for adding and removing random characters (salt) to/from text.

    Attributes:
        position (str): The position to add salt ('front', 'end', 'between').
        random_state (tuple): The state of the random number generator.
        characters (list): The list of characters to use for salting.
        min_length (int): The minimum length of the salt.
        max_length (int): The maximum length of the salt.

    Methods:
        encode(text): Adds salt to the text.
        decode(text): Removes salt from the text.
    """

    def __init__(self, position: str = 'between', random_seed: int = 42, min_length: int = 2, max_length: int = 7):
        """
        Initializes the Salt class with the given parameters.

        Args:
            position (str): The position to add salt ('front', 'end', 'between').
            random_seed (int): The seed for the random number generator.
            min_length (int): The minimum length of the salt.
            max_length (int): The maximum length of the salt.

        Raises:
            ValueError: If the position is not 'front', 'end', or 'between'.
        """
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
        """
        Adds salt to the text.

        Args:
            text (str): The text to be salted.

        Returns:
            str: The salted text.
        """
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
        """
        Removes salt from the text.

        Args:
            text (str): The text to be desalted.

        Returns:
            str: The desalted text.
        """
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
        """
        Generates a random string of characters to be used as salt.

        Returns:
            str: The generated salt.
        """
        return ''.join(random.choices(self.characters, k=random.randint(self.min_length, self.max_length)))


class StructuredDataEncoder:
    """
    A class for encoding and decoding structured data (lists, tuples, dicts, sets).

    Attributes:
        encoder (object): The encoder object to be used for encoding and decoding.

    Methods:
        encode(data): Encodes the given structured data.
        decode(data): Decodes the given structured data.
    """

    def __init__(self, encoder: object):
        """
        Initializes the StructuredDataEncoder with the given encoder.

        Args:
            encoder (object): The encoder object to be used for encoding and decoding.
        """
        self.encoder = encoder

    def encode(self, data: object) -> object:
        """
        Encodes the given structured data.

        Args:
            data (object): The data to be encoded.

        Returns:
            object: The encoded data.
        """
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
        """
        Decodes the given structured data.

        Args:
            data (object): The data to be decoded.

        Returns:
            object: The decoded data.

        Raises:
            ValueError: If the data type is not supported.
        """
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
        """
        Encodes or decodes a list.

        Args:
            data (list): The list to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            list: The encoded or decoded list.
        """
        new_list = []
        for index, datum in enumerate(data):
            if mode == 'encode':
                new_list.append(self.encode(datum))
            else:
                new_list.append(self.decode(datum))

        return new_list

    def __tuple_encoder(self, data: tuple, mode: str = 'encode') -> tuple:
        """
        Encodes or decodes a tuple.

        Args:
            data (tuple): The tuple to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            tuple: The encoded or decoded tuple.
        """
        return tuple(self.__list_encoder(list(data), mode=mode))

    def __dict_encoder(self, data: dict, mode: str = 'encode') -> dict:
        """
        Encodes or decodes a dictionary.

        Args:
            data (dict): The dictionary to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            dict: The encoded or decoded dictionary.
        """
        new_dict = {}
        for key, value in data.items():
            if mode == 'encode':
                new_dict[self.encode(key)] = self.encode(value)
            else:
                new_dict[self.decode(key)] = self.decode(value)

        return new_dict

    def __set_encoder(self, data: set, mode: str = 'encode') -> set:
        """
        Encodes or decodes a set.

        Args:
            data (set): The set to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            set: The encoded or decoded set.
        """
        new_set = set({})
        for element in data:
            if mode == 'encode':
                new_set.add(self.encode(element))
            else:
                new_set.add(self.decode(element))

        return new_set

    def __frozen_set_encoder(self, data: frozenset, mode: str = 'encode') -> frozenset:
        """
        Encodes or decodes a frozenset.

        Args:
            data (frozenset): The frozenset to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            frozenset: The encoded or decoded frozenset.
        """
        return frozenset(self.__set_encoder(set(data), mode=mode))

    def __get_str(self, obj: object) -> str:
        """
        Converts an object to its string representation.

        Args:
            obj (object): The object to be converted.

        Returns:
            str: The string representation of the object.

        Raises:
            ValueError: If the data type is not supported.
        """
        if isinstance(obj, (int, float, complex, bool, type(None), range, bytes, bytearray)):
            return str(obj)
        elif isinstance(obj, str):
            return f'str(\'{obj}\')'
        else:
            raise ValueError(f"Data type '{obj}' is not supported.")


class TextFileEncoder:
    """
    A class for encoding and decoding text files.

    Attributes:
        encoder (object): The encoder object to be used for encoding and decoding.

    Methods:
        encode(file, file_out): Encodes the content of a text file.
        decode(file, file_out): Decodes the content of a text file.
    """

    def __init__(self, encoder: object):
        """
        Initializes the TextFileEncoder with the given encoder.

        Args:
            encoder (object): The encoder object to be used for encoding and decoding.
        """
        self.encoder = encoder

    def encode(self, file: str, file_out: str = None) -> None:
        """
        Encodes the content of a text file.

        Args:
            file (str): The path to the input file.
            file_out (str): The path to the output file. If None, the input file will be overwritten.

        Raises:
            ValueError: If the file extensions are not '.txt'.
        """
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
        """
        Decodes the content of a text file.

        Args:
            file (str): The path to the input file.
            file_out (str): The path to the output file. If None, the input file will be overwritten.

        Raises:
            ValueError: If the file extensions are not '.txt'.
        """
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
    """
    A class for encoding and decoding JSON files.

    Attributes:
        encoder (StructuredDataEncoder): The encoder object to be used for encoding and decoding.

    Methods:
        encode(file, file_out, indent): Encodes the content of a JSON file.
        decode(file, file_out, indent): Decodes the content of a JSON file.
    """

    def __init__(self, encoder: object):
        """
        Initializes the JSONFileEncoder with the given encoder.

        Args:
            encoder (object): The encoder object to be used for encoding and decoding.
        """
        self.encoder = StructuredDataEncoder(encoder=encoder)

    def encode(self, file: str, file_out: str = None, indent: int = 4) -> None:
        """
        Encodes the content of a JSON file.

        Args:
            file (str): The path to the input file.
            file_out (str): The path to the output file. If None, the input file will be overwritten.
            indent (int): The number of spaces to use for indentation in the output file.

        Raises:
            ValueError: If the file extensions are not '.json'.
        """
        if file[file.rindex('.') + 1:] != 'json' or (file_out[file_out.rindex('.') + 1:] != 'json' if file_out else False):
            raise ValueError("JSONFileEncoder only supports text files with extension: '.json'")

        with open(file, 'r') as f:
            data = json.load(f)

        enc_data = self.encoder.encode(data)

        with open(file_out if file_out else file, 'w') as f:
            json.dump(enc_data, f, indent=indent)

    def decode(self, file: str, file_out: str = None, indent: int = 4) -> None:
        """
        Decodes the content of a JSON file.

        Args:
            file (str): The path to the input file.
            file_out (str): The path to the output file. If None, the input file will be overwritten.
            indent (int): The number of spaces to use for indentation in the output file.

        Raises:
            ValueError: If the file extensions are not '.json'.
        """
        if file[file.rindex('.') + 1:] != 'json' or (file_out[file_out.rindex('.') + 1:] != 'json' if file_out else False):
            raise ValueError("JSONFileEncoder only supports text files with extension: '.json'")

        with open(file, 'r') as f:
            data = json.load(f)

        dec_data = self.encoder.decode(data)

        with open(file_out if file_out else file, 'w') as f:
            json.dump(dec_data, f, indent=indent)
