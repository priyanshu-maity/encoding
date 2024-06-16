import unittest
import json

from encoding.utils import TextEncoder, Pipeline, Salt, StructuredDataEncoder, TextFileEncoder, JSONFileEncoder
from encoding.ciphers.substitution import CaesarCipher, AtbashCipher, AffineCipher, VigenereCipher
from encoding.ciphers.transposition import RailFenceCipher, ColumnarTranspositionCipher


global_pipeline = Pipeline([
        (Salt(), 'salt'),
        (RailFenceCipher(), 'rail_fence'),
        (CaesarCipher(), 'caesar'),
        (VigenereCipher(), 'vigenere')
    ])

sample_strings = [
    "Hello, World!",
    '12345',
    'Random Characters: !@#$%^&*()_+-=',
    "I'm learning Python.",
    ""
]


class TestPipeline(unittest.TestCase):
    def test_encode_without_salt(self):
        pipeline = Pipeline([
            (CaesarCipher(), 'caesar_cipher'),
            (RailFenceCipher(), 'rail_cipher'),
            (VigenereCipher(), 'vigenere_cipher')
        ])

        for sample_string in sample_strings:
            enc_text = pipeline.encode(sample_string)
            dec_text = pipeline.decode(enc_text)

            self.assertEqual(sample_string, dec_text)

    def test_encode_with_salt(self):
        pipeline = Pipeline([
            (Salt(), 'salt'),
            (CaesarCipher(), 'caesar_cipher'),
            (RailFenceCipher(), 'rail_cipher'),
            (VigenereCipher(), 'vigenere_cipher')
        ])

        for sample_string in sample_strings:
            enc_text = pipeline.encode(sample_string)
            dec_text = pipeline.decode(enc_text)

            self.assertEqual(sample_string, dec_text)

    def test_add_encoders(self):
        pipeline = Pipeline([
            (CaesarCipher(), 'caesar_cipher'),
            (RailFenceCipher(), 'rail_cipher')
        ])

        pipeline.add_encoders([
            (Salt(), 'salt'),
            (VigenereCipher(), 'vigenere_cipher')
        ])

        self.assertEqual(pipeline.encoder_names, ['caesar_cipher', 'rail_cipher', 'salt', 'vigenere_cipher'])

    def test_remove_encoders(self):
        pipeline = Pipeline([
            (Salt(), 'salt'),
            (CaesarCipher(), 'caesar_cipher'),
            (RailFenceCipher(), 'rail_cipher'),
            (VigenereCipher(), 'vigenere_cipher')
        ])

        pipeline.remove_encoders(['salt', 'vigenere_cipher'])

        self.assertEqual(pipeline.encoder_names, ['caesar_cipher', 'rail_cipher'])


class TestSalt(unittest.TestCase):
    def test_salt_front(self):
        salt = Salt(position='front')

        for sample_string in sample_strings:
            salted_text = salt.encode(sample_string)
            desaulted_text = salt.decode(salted_text)

            self.assertEqual(sample_string, desaulted_text)

    def test_salt_end(self):
        salt = Salt(position='end')

        for sample_string in sample_strings:
            salted_text = salt.encode(sample_string)
            desaulted_text = salt.decode(salted_text)

            self.assertEqual(sample_string, desaulted_text)
    def test_salt_between(self):
        salt = Salt(position='between')

        for sample_string in sample_strings:
            salted_text = salt.encode(sample_string)
            desaulted_text = salt.decode(salted_text)

            self.assertEqual(sample_string, desaulted_text)


class TestSDE(unittest.TestCase):
    def test_list(self):
        sample_list = [42, 3.14, True, "Hello, World!", ['apple', 'banana'], ('one', 'two', 'three'),
                       {'name': 'Alice', 'age': 30}, {1, 2, 3}, b'bytes', bytearray(b'bytearray'), None]

        encoder = StructuredDataEncoder(encoder=global_pipeline)
        enc_list = encoder.encode(sample_list)
        dec_list = encoder.decode(enc_list)

        self.assertEqual(sample_list, dec_list)

    def test_tuple(self):
        sample_tuple = (42, 3.14, True, "Hello, World!", ['apple', 'banana'], ('one', 'two', 'three'),
                        {'name': 'Alice', 'age': 30}, {1, 2, 3}, b'bytes', bytearray(b'bytearray'), None)

        encoder = StructuredDataEncoder(encoder=global_pipeline)
        enc_tuple = encoder.encode(sample_tuple)
        dec_tuple = encoder.decode(enc_tuple)

        self.assertEqual(sample_tuple, dec_tuple)

    def test_dict(self):
        sample_dict = {
            'name': 'John Doe',
            'age': 30,
            'city': 'New York',
            'is_student': False,
            'grades': [85, 92, 78, 90],
            'address': {
                'street': '123 Main St',
                'zip_code': '10001',
                'state': 'NY'
            }
        }

        encoder = StructuredDataEncoder(encoder=global_pipeline)
        enc_dict = encoder.encode(sample_dict)
        dec_dict = encoder.decode(enc_dict)

        self.assertEqual(sample_dict, dec_dict)

    def test_set(self):
        sample_set = {1, 2.5, 'apple', (3, 4), True}

        encoder = StructuredDataEncoder(encoder=global_pipeline)
        enc_set = encoder.encode(sample_set)
        dec_set = encoder.decode(enc_set)

        self.assertEqual(sample_set, dec_set)

    def test_frozenset(self):
        sample_set = frozenset({1, 2.5, 'apple', (3, 4), True})

        encoder = StructuredDataEncoder(encoder=global_pipeline)
        enc_set = encoder.encode(sample_set)
        dec_set = encoder.decode(enc_set)

        self.assertEqual(sample_set, dec_set)


class TestTFE(unittest.TestCase):
    def test(self):
        encoder = TextFileEncoder(encoder=global_pipeline)

        with open("sample_text_file.txt", 'r') as file:
            sample_text = file.read()

        encoder.encode(file="sample_text_file.txt")
        encoder.decode(file="sample_text_file.txt")

        with open("sample_text_file.txt", 'r') as file:
            decoded_text = file.read()

        self.assertEqual(sample_text, decoded_text)


class TestJFE(unittest.TestCase):
    def test(self):
        encoder = JSONFileEncoder(encoder=global_pipeline)

        with open("sample_json_file.json", 'r') as file:
            sample_json = json.load(file)

        encoder.encode(file="sample_json_file.json")
        encoder.decode(file="sample_json_file.json")

        with open("sample_json_file.json", 'r') as file:
            decoded_json = json.load(file)

        self.assertEqual(sample_json, decoded_json)


if __name__ == '__main__':
    unittest.main()
