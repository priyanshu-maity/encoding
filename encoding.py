import inspect


class TextEncoder(type):
    def __new__(cls, name, bases, dct):
        if 'encode' not in dct or 'decode' not in dct:
            raise TypeError(f"Class {name} must implement both encode and decode methods")

        if not callable(dct['encode']) or not callable(dct['decode']):
            raise TypeError(f"Both encode and decode must be callable")

        check_methods = ['encode', 'decode']
        for method in check_methods:
            signature = inspect.signature(dct[method])
            expected_params = {'self', 'text'}
            params = set(signature.parameters.keys())
            if not expected_params.issubset(params) or signature.return_annotation != str:
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
            self.encoder_names.append(encoder[1])
