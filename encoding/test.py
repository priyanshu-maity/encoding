from utils import JSONFileEncoder, Pipeline, Salt
from text.substitution import CaesarCipher, VigenereCipher
from text.transposition import RailFenceCipher, ColumnarTranspositionCipher


pipeline = Pipeline([
    (Salt(min_length=2, max_length=3, random_seed=50), 'salt'),
    (RailFenceCipher(rails=2), 'rail_fence'),
    (CaesarCipher(), 'caesar'),
    (VigenereCipher(), 'vigenere')
])

encoder = JSONFileEncoder(encoder=pipeline)
encoder.decode(file="themes2.json")
