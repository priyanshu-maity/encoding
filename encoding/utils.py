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

from tqdm import tqdm


class TextEncoder(type):
    """
    Metaclass for enforcing requirements on subclasses implementing encoding and decoding methods.

    This metaclass ensures that subclasses implement both an `encode` and a `decode` method,
    and that these methods adhere to a specific signature and return type.

    Methods:
        - __new__(cls, name, bases, dct) -> type: Creates a new class object.
            Raises TypeError if either `encode` or `decode` method is missing in the class,
            or if these methods are not callable, or if they do not have the correct signature
            (taking `self` and `text` parameters and returning a string).
    """

    def __new__(cls, name, bases, dct):
        """
        Creates a new class object.

        Parameters:
            - name (str): The name of the class being created.
            - bases (tuple): The base classes of the class being created.
            - dct (dict): The dictionary containing the attributes of the class being created.

        Returns:
            - type: The newly created class object.

        Raises:
            - TypeError: If either `encode` or `decode` method is missing in the class,
              or if these methods are not callable, or if they do not have the correct signature
              (taking `self` and `text` parameters and returning a string).
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
    A class for creating and applying pipelines to encode and decode text using multiple encoders.

    Attributes:
        - encoder_names (list): A list of names of the encoders in the pipeline.

    Methods:
        - __init__(self, encoders: list): Initializes the Pipeline object with a list of encoders.
        - encode(self, text: str) -> str: Encodes the input text using the encoders in the pipeline.
        - decode(self, text: str) -> str: Decodes the input text using the encoders in reverse order.
        - add_encoders(self, encoders: list): Adds additional encoders to the pipeline.
        - remove_encoders(self, encoder_names: list): Removes encoders from the pipeline by their names.

    Private Methods:
        - __is_valid(self, encoders) -> bool: Checks if the format of the encoders is valid.
        - __get_encoder_names(self): Retrieves and updates the list of encoder names.

    Raises:
        - ValueError: If the format of the encoders is invalid or if there are duplicate encoder names.
    """

    def __init__(self, encoders: list):
        """
        Initializes the Pipeline object with a list of encoders.

        Parameters:
            - encoders (list): A list of tuples containing encoder class objects and their names.

        Raises:
            - ValueError: If the format of the encoders is invalid.
        """

        self.encoder_names = []

        if self.__is_valid(encoders):
            self.encoders = encoders
            self.__get_encoder_names()
        else:
            raise ValueError("Encoders must be passed as a tuple of class object and names of the encoders.")

    def encode(self, text: str) -> str:
        """
        Encodes the input text using the encoders in the pipeline.

        Parameters:
            - text (str): The input text to be encoded.

        Returns:
            - str: The encoded text.
        """

        for encoder in self.encoders:
            text = encoder[0].encode(text)

        return text

    def decode(self, text: str) -> str:
        """
        Decodes the input text using the encoders in reverse order.

        Parameters:
            - text (str): The input text to be decoded.

        Returns:
            - str: The decoded text.
        """

        for decoder in self.encoders[::-1]:
            text = decoder[0].decode(text)

        return text

    def add_encoders(self, encoders: list):
        """
        Adds additional encoders to the pipeline.

        Parameters:
            - encoders (list): A list of tuples containing additional encoder class objects and their names.

        Raises:
            - ValueError: If the format of the encoders is invalid.
        """

        if self.__is_valid(encoders):
            self.encoders.extend(encoders)
            self.__get_encoder_names()
        else:
            raise ValueError("Encoders must be passed as tuples of class object and names of the encoders.")

    def remove_encoders(self, encoder_names: list):
        """
        Removes encoders from the pipeline by their names.

        Parameters:
            - encoder_names (list): A list of names of the encoders to be removed.

        Raises:
            - ValueError: If the provided encoder names are invalid or if the encoders are not found in the pipeline.
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
        Checks if the format of the encoders is valid.

        Parameters:
            - encoders: A list of tuples containing encoder class objects and their names.

        Returns:
            - bool: True if the format is valid, False otherwise.
        """

        for encoder in encoders:
            if len(encoder) != 2:
                return False

            if type(encoder[1]) != str:
                return False

        return True

    def __get_encoder_names(self):
        """
        Retrieves and updates the list of encoder names.
        """

        self.encoder_names.clear()
        for encoder in self.encoders:
            if encoder in self.encoder_names:
                raise ValueError(f"Two encoders cannot have the same name: {encoder}.")
            self.encoder_names.append(encoder[1])


class Salt:
    """
    A class for adding and removing salt from text before encoding and after decoding.

    Attributes:
        - random_state (tuple): The random state used for generating salt.
        - characters (list): A list of characters used for generating salt.
        - min_length (int): The minimum length of salt.
        - max_length (int): The maximum length of salt.
        - position (str): The position at which salt is added ('front', 'end', or 'between').

    Methods:
        - __init__(self, position: str = 'between', random_seed: int = 42, min_length: int = 2, max_length: int = 7):
            Initializes the Salt object with the specified parameters.
        - encode(self, text: str) -> str: Adds salt to the input text based on the specified position.
        - decode(self, text: str) -> str: Removes salt from the input text based on the specified position.

    Private Methods:
        - __get_salt(self) -> str: Generates random salt of variable length.
    """

    def __init__(self, position: str = 'between', random_seed: int = 42, min_length: int = 2, max_length: int = 7):
        """
        Initializes the Salt object with the specified parameters.

        Parameters:
            - position (str): The position at which salt is added ('front', 'end', or 'between') (default: 'between').
            - random_seed (int): The random seed for generating salt (default: 42).
            - min_length (int): The minimum length of salt (default: 2).
            - max_length (int): The maximum length of salt (default: 7).

        Raises:
            - ValueError: If an invalid salt position is provided.
        """

        random.seed(random_seed)
        self.random_state = random.getstate()
        self.characters = [chr(i) for i in range(33, 127)]
        self.min_length = min_length
        self.max_length = max_length
        self.positions = ['front', 'end', 'between']

        if position in self.positions:
            self.position = position
        else:
            raise ValueError(f"Salt position cannot be '{position}'. Valid salt positons: {', '.join(self.positions)}")

    def encode(self, text: str) -> str:
        """
        Adds salt to the input text based on the specified position.

        Parameters:
            - text (str): The input text to which salt is added.

        Returns:
            - str: The text with salt added.
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
        Removes salt from the input text based on the specified position.

        Parameters:
            - text (str): The input text from which salt is removed.

        Returns:
            - str: The text with salt removed.
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
        Generates random salt of variable length.

        Returns:
            - str: The randomly generated salt.
        """

        return ''.join(random.choices(self.characters, k=random.randint(self.min_length, self.max_length)))


class TextFileEncoder:
    """
    A class for encoding and decoding text files using a specified encoder.

    Attributes:
        - encoder (object): The encoder/pipeline object used for encoding and decoding.

    Methods:
        - __init__(self, encoder: object): Initializes the FileEncoder object with the specified encoder.
        - encode(self, file: str, file_out: str = None, progressbar: bool = False) -> None:
            Encodes the contents of a text file and writes the encoded text to the same or another file.
        - decode(self, file: str, file_out: str = None, progressbar: bool = False) -> None:
            Decodes the contents of an encoded text file and writes the decoded text to the same or another file.
    """

    def __init__(self, encoder: object):
        """
        Initializes the FileEncoder object with the specified encoder.

        Parameters:
            - encoder (object): The encoder/pipeline object used for encoding and decoding.
        """

        self.encoder = encoder

    def encode(self, file: str, file_out: str = None, progressbar: bool = False) -> None:
        """
        Encodes the contents of a text file and writes the encoded text to the same or another file.

        Parameters:
            - file (str): The path to the input text file to be encoded.
            - file_out (str): The path to the output text file where the encoded text will be written
              (default: None, which overwrites the input file).
            - progressbar (bool): Whether to display a progress bar during encoding (default: False).

        Raises:
            - ValueError: If the files are not text files.
        """

        enc_text = ''

        if file[file.rindex('.') + 1:] != 'txt' or file_out[file_out.rindex('.') + 1:] != 'txt':
            raise ValueError("TextFileEncoder only supports text files with extension: '.txt'")

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

    def decode(self, file: str, file_out: str = None, progressbar: bool = False) -> None:
        """
        Decodes the contents of an encoded text file and writes the decoded text to the same or another file.

        Parameters:
            - file (str): The path to the input text file to be decoded.
            - file_out (str): The path to the output text file where the decoded text will be written
              (default: None, which overwrites the input file).
            - progressbar (bool): Whether to display a progress bar during decoding (default: False).

        Raises:
            - ValueError: If the files are not text files.
        """

        dec_text = ''

        if file[file.rindex('.') + 1:] != 'txt' or file_out[file_out.rindex('.') + 1:] != 'txt':
            raise ValueError("TextFileEncoder only supports text files with extension: '.txt'")

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
