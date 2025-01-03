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

import random
import json
from pathlib import Path
from typing import Optional, Self, Any
from abc import ABC, abstractmethod
from enum import Enum


class TextEncoder(ABC):
    """
    Abstract base class to enforce implementation of `encode` and `decode` methods.
    """

    @abstractmethod
    def encode(self: Self, text: str) -> str:
        """
        Abstract method to be implemented by subclasses for encoding text.
        Args:
            text (str): The text to encode.
        Returns:
            str: The encoded text.
        """
        pass

    @abstractmethod
    def decode(self: Self, text: str) -> str:
        """
        Abstract method to be implemented by subclasses for decoding text.
        Args:
            text (str): The text to decode.
        Returns:
            str: The decoded text.
        """
        pass


class Pipeline(TextEncoder):
    """
    A class for managing a sequence of encoders and applying them to text.

    Attributes:
        encoders (list[tuple[TextEncoder | Pipeline, str]]): A list of encoder classes and their names.
        encoder_names (list[str]): A list of encoder names.

    Methods:
        encode(text): Encodes the given text using the sequence of encoders.
        decode(text): Decodes the given text using the sequence of decoders.
        add_encoders(encoders): Adds more encoders to the sequence.
        remove_encoders(encoder_names): Removes encoders from the sequence by their names.
    """

    def __init__(self: Self, encoders: list[tuple[TextEncoder | "Pipeline", str]]):
        """
        Initializes the Pipeline with a list of encoders.

        Args:
            encoders (list[tuple[TextEncoder, str]]): A list of tuples containing encoder class objects and their names.

        Raises:
            ValueError: If the encoders are not passed as a list of tuples with class object and name.
        """
        self.encoder_names: list[str] = []

        if self.__is_valid(encoders):
            self.encoders: list[tuple[TextEncoder | "Pipeline", str]] = encoders
            self.__update_encoder_names()
        else:
            raise ValueError("Encoders must be passed as a tuple of class object and names of the encoders.")

    def encode(self: Self, text: str) -> str:
        """
        Encodes the given text using the sequence of encoders.

        Args:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.
        """
        for encoder in self.encoders:
            text: str = encoder[0].encode(text)

        return text

    def decode(self: Self, text: str) -> str:
        """
        Decodes the given text using the sequence of decoders.

        Args:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.
        """
        for decoder in self.encoders[::-1]:
            text: str = decoder[0].decode(text)

        return text

    def add_encoders(self: Self, encoders: list[tuple[TextEncoder | "Pipeline", str]]):
        """
        Adds more encoders to the sequence.

        Args:
            encoders (list[tuple[TextEncoder | "Pipeline", str]]): A list of tuples containing encoder class objects and their names.

        Raises:
            ValueError: If the encoders are not passed as tuples of class object and names.
        """
        if self.__is_valid(encoders):
            self.encoders.extend(encoders)
            self.__update_encoder_names()
        else:
            raise ValueError("Encoders must be passed as tuples of class object and names of the encoders.")

    def remove_encoders(self: Self, encoder_names: list[str]):
        """
        Removes encoders from the sequence by their names.

        Args:
            encoder_names (list[str]): A list of encoder names to be removed.

        Raises:
            ValueError: If encoder names are not strings or are not found in the original list of encoders.
        """
        for encoder_name in encoder_names:
            if type(encoder_name) != str:
                raise ValueError("Encoders must be passed as a list of encoder names.")
            if encoder_name not in self.encoder_names:
                raise ValueError("Encoder names given are unavailable in original list of encoders.")

        temp_encoders: list[tuple[TextEncoder, str]] = []
        for encoder in self.encoders:
            if encoder[1] not in encoder_names:
                temp_encoders.append(encoder)

        self.encoders = temp_encoders
        self.__update_encoder_names()

    def __is_valid(self: Self, encoders) -> bool:
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

    def __update_encoder_names(self: Self):
        """
        Updates the list of encoder names.
        """
        self.encoder_names.clear()
        for encoder in self.encoders:
            if encoder in self.encoder_names:
                raise ValueError(f"Two encoders cannot have the same name: {encoder}.")
            self.encoder_names.append(encoder[1])


# TODO: Update Salt class structure and functioning
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

    def __init__(self: Self, position: str = 'between', random_seed: int = 42, min_length: int = 2, max_length: int = 7):
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

    def encode(self: Self, text: str) -> str:
        """
        Adds salt to the text.

        Args:
            text (str): The text to be salted.

        Returns:
            str: The salted text.
        """
        if text == '':
            return text

        random.setstate(self.random_state)
        
        if self.position == 'front':
            return self.__get_salt() + text

        elif self.position == 'end':
            return text + self.__get_salt()

        elif self.position == 'between':
            salts = []
            for i in range(len(text)):
                salts.append(self.__get_salt())
            return ''.join([text[i] + salts[i] for i in range(len(salts))])

    def decode(self: Self, text: str) -> str:
        """
        Removes salt from the text.

        Args:
            text (str): The text to be desalted.

        Returns:
            str: The desalted text.
        """
        if text == '':
            return text

        random.setstate(self.random_state)
        
        if self.position == 'front':
            return text.removeprefix(self.__get_salt())

        if self.position == 'end':
            return text.removesuffix(self.__get_salt())

        if self.position == 'between':
            pure_text = ''
            try:
                i = 0
                while True:
                    pure_text += text[i]
                    i += len(self.__get_salt()) + 1
            except IndexError:
                return pure_text

    def __get_salt(self: Self) -> str:
        """
        Generates a random string of characters to be used as salt.

        Returns:
            str: The generated salt.
        """
        return ''.join(random.choices(self.characters, k=random.randint(self.min_length, self.max_length)))


class StructuredDataEncoder:
    """
    A class for encoding and decoding structured data (lists, tuples, dicts, sets and frozen sets).

    Attributes:
        encoder (TextEncoder): The encoder object to be used for encoding and decoding.

    Methods:
        encode(data): Encodes the given structured data.
        decode(data): Decodes the given structured data.
    """

    def __init__(self: Self, encoder: TextEncoder):
        """
        Initializes the StructuredDataEncoder with the given encoder.

        Args:
            encoder (TextEncoder): The encoder object to be used for encoding and decoding.
        """
        self.encoder: TextEncoder = encoder

    def encode(self: Self, data: Any) -> Any:
        """
        Encodes the given structured data.

        Args:
            data (Any): The data to be encoded.

        Returns:
            Any: The encoded data.
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

    def decode(self: Self, data: Any) -> Any:
        """
        Decodes the given structured data.

        Args:
            data (Any): The data to be decoded.

        Returns:
            Any: The decoded data.

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
            raise ValueError(f"Data type '{type(data)}' is not supported.")

    def __list_encoder(self: Self, data: list, mode: str) -> list:
        """
        Encodes or decodes a list.

        Args:
            data (list): The list to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            list: The encoded or decoded list.
        """
        new_list: list[Any] = []
        for index, datum in enumerate(data):
            if mode == 'encode':
                new_list.append(self.encode(datum))
            else:
                new_list.append(self.decode(datum))

        return new_list

    def __tuple_encoder(self: Self, data: tuple, mode: str) -> tuple:
        """
        Encodes or decodes a tuple.

        Args:
            data (tuple): The tuple to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            tuple: The encoded or decoded tuple.
        """
        return tuple(self.__list_encoder(list(data), mode=mode))

    def __dict_encoder(self: Self, data: dict, mode: str) -> dict:
        """
        Encodes or decodes a dictionary.

        Args:
            data (dict): The dictionary to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            dict: The encoded or decoded dictionary.
        """
        new_dict: dict[Any] = {}
        for key, value in data.items():
            if mode == 'encode':
                new_dict[self.encode(key)] = self.encode(value)
            else:
                new_dict[self.decode(key)] = self.decode(value)

        return new_dict

    def __set_encoder(self: Self, data: set, mode: str) -> set:
        """
        Encodes or decodes a set.

        Args:
            data (set): The set to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            set: The encoded or decoded set.
        """
        new_set: set[Any] = set()
        for element in data:
            if mode == 'encode':
                new_set.add(self.encode(element))
            else:
                new_set.add(self.decode(element))

        return new_set

    def __frozen_set_encoder(self: Self, data: frozenset, mode: str) -> frozenset:
        """
        Encodes or decodes a frozenset.

        Args:
            data (frozenset): The frozenset to be encoded or decoded.
            mode (str): The mode of operation ('encode' or 'decode').

        Returns:
            frozenset: The encoded or decoded frozenset.
        """
        return frozenset(self.__set_encoder(set(data), mode=mode))

    @staticmethod
    def __get_str(obj: Any) -> str:
        """
        Converts an object to its string representation.

        Args:
            obj (Any): The object to be converted.

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
            raise ValueError(f"Data type '{type(obj)}' is not supported.")


class InputType(Enum):
    PATH: str = "path"
    STR: str = "str"
    DICT: str = "dict"


class TextFileEncoder:
    """
    A class for encoding and decoding text files.

    Attributes:
        encoder (TextEncoder | Pipeline): The encoder object to be used for encoding and decoding.

    Methods:
        encode(input_data, input_type, write_to, return_text): Encodes the content of a text file.
        decode(input_data, input_type, write_to, return_text): Decodes the content of a text file.
    """

    def __init__(self: Self, encoder: TextEncoder | Pipeline) -> None:
        """
        Initializes the TextFileEncoder with the given encoder.

        Args:
            encoder (TextEncoder | Pipeline): The encoder object to be used for encoding and decoding.
        """
        self.encoder: TextEncoder | Pipeline = encoder

    def encode(
            self: Self,
            input_data: Path | str,
            input_type: InputType,
            write_to: Optional[Path | str] = None,
            return_text: bool = True
    ) -> str | None:
        """
        Encodes the content of a text file.

        Args:
            input_data (Path | str): The text or the file path containing the text to be encoded.
            input_type (InputType): The input type of the input which is either a string or file path.
            write_to (Path | str): The file path to store the encoded text.
            return_text (bool): Returns the encoded text if set to True (default: True).

        Raises:
            ValueError: If anything else is passed, other than text file path or string.
        """
        enc_text: list[str] = []

        if input_type.value == "str" and isinstance(input_data, str):
            lines = input_data.splitlines()
            for line in lines:
                enc_text.append(self.encoder.encode(line))
        elif input_type.value == "path" and isinstance(input_data, Path | str):
            with open(input_data, 'r') as file:
                for line in file:
                    enc_text.append(self.encoder.encode(line.rstrip('\n')))
        else:
            raise ValueError("input_data in TextFileEncoder only supports text file paths and strings.")

        encoded_result: str = '\n'.join(enc_text)

        if write_to is not None:
            with open(write_to, 'w') as file:
                file.write(encoded_result)
                file.write('\n')

        if return_text:
            return encoded_result

    def decode(
            self: Self,
            input_data: Path | str,
            input_type: InputType,
            write_to: Optional[Path | str] = None,
            return_text: bool = True
    ) -> str | None:
        """
        Decodes the content of a text file.

        Args:
            input_data (Path | str): The text or the file path containing the text to be decoded.
            input_type (InputType): The input type of the input which is either a string or file path.
            write_to (Path | str): The file path to store the decoded text.
            return_text (bool): Returns the decoded text if set to True (default: True).

        Raises:
            ValueError: If anything else is passed, other than text file path or string.
        """
        dec_text: list[str] = []

        if input_type.value == "str" and isinstance(input_data, str):
            lines: list[str] = input_data.splitlines()
            for line in lines:
                dec_text.append(self.encoder.decode(line))
        elif input_type.value == "path" and isinstance(input_data, Path | str):
            with open(input_data, 'r') as file:
                for line in file:
                    dec_text.append(self.encoder.decode(line.rstrip('\n')))
        else:
            raise ValueError("input_data in TextFileEncoder only supports text file paths and strings.")

        decoded_result: str = '\n'.join(dec_text)

        if write_to is not None:
            with open(write_to, 'w') as file:
                file.write(decoded_result)
                file.write('\n')

        if return_text:
            return decoded_result


class JSONFileEncoder:
    """
    A class for encoding and decoding JSON files.

    Attributes:
        encoder (TextEncoder | Pipeline): The encoder object to be used for encoding and decoding.

    Methods:
        encode(data, file_out, return_text, indent): Encodes the content of a JSON file.
        decode(data, file_out, return_text, indent): Decodes the content of a JSON file.
    """

    def __init__(self, encoder: TextEncoder | Pipeline):
        """
        Initializes the JSONFileEncoder with the given encoder.

        Args:
            encoder (TextEncoder | Pipeline): The encoder object to be used for encoding and decoding.
        """
        self.encoder = StructuredDataEncoder(encoder=encoder)

    def encode(
            self: Self,
            input_data: Path | str | dict,
            input_type: InputType,
            write_to: Optional[Path | str] = None,
            indent: int = 4,
            return_dict: bool = True
    ) -> dict | None:
        """
        Encodes the content of a JSON file.

        Args:
            input_data (Path | str | dict): The dictionary or the JSON file path to be encoded.
            input_type (InputType): The input type of the input which is either a dictionary or file path.
            write_to (Optional[Path | str]): The file path to store the encoded JSON.
            indent (int): The number of spaces to use for indentation in the output file (default: 4).
            return_dict (bool): Returns the encoded dictionary if set to True (default: True).

        Raises:
            ValueError: If anything else is passed, other than JSON object or string.
        """
        if input_type.value == "path" and isinstance(input_data, Path | str):
            with open(input_data, 'r') as json_file:
                input_data = json.load(json_file)
        elif not input_type.value == "dict" or not isinstance(input_data, dict):
            raise ValueError("input_data in JSONFileEncoder only supports JSON files and dictionaries")

        enc_data = self.encoder.encode(input_data)

        if write_to is not None:
            with open(write_to, 'w') as json_file:
                json.dump(enc_data, json_file, indent=indent)

        if return_dict:
            return enc_data

    def decode(
            self: Self,
            input_data: Path | str | dict,
            input_type: InputType,
            write_to: Optional[Path | str] = None,
            indent: int = 4,
            return_dict: bool = True
    ) -> dict | None:
        """
        Decodes the content of a JSON file.

        Args:
            input_data (Path | str | dict): The dictionary or the JSON file path to be decoded.
            input_type (InputType): The input type of the input which is either a dictionary or file path.
            write_to (Optional[Path | str]): The file path to store the decoded JSON.
            indent (int): The number of spaces to use for indentation in the output file (default: 4).
            return_dict (bool): Returns the encoded dictionary if set to True (default: True).

        Raises:
            ValueError: If anything else is passed, other than JSON object or string.
        """
        if input_type.value == "path" and isinstance(input_data, Path | str):
            with open(input_data, 'r') as json_file:
                input_data = json.load(json_file)
        elif not input_type.value == "dict" or not isinstance(input_data, dict):
            raise ValueError("input_data in JSONFileEncoder only supports JSON files and dictionaries")

        dec_data = self.encoder.decode(input_data)

        if write_to is not None:
            with open(write_to, 'w') as json_file:
                json.dump(dec_data, json_file, indent=indent)

        if return_dict:
            return dec_data
