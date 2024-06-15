from utils import StructuredDataEncoder, Pipeline, Salt
from text.substitution import CaesarCipher, VigenereCipher
from text.transposition import RailFenceCipher, ColumnarTranspositionCipher

import json


pipeline = Pipeline([
    (Salt(min_length=2, max_length=3, random_seed=50), 'salt'),
    (RailFenceCipher(key=2), 'rail_fence'),
    (ColumnarTranspositionCipher(), 'ctc'),
    (CaesarCipher(), 'caesar'),
    (VigenereCipher(), 'vigenere')
])

data_tuple = (
    "Hello, world!",  # String
    42,               # Integer
    3.14159,          # Float
    ["apple", "banana", "cherry"],  # List
    {"name": "Alice", "age": 30},   # Dictionary
    (1, 2, 3)         # Another tuple
)

encoder = StructuredDataEncoder(encoder=pipeline)

enc_list = encoder.encode(data_tuple)
print("Encoded List:", enc_list, end="\n\n")

dec_list = encoder.decode(enc_list)
print("Decoded List:", dec_list)
