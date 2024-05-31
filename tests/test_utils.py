import unittest

from encoding.utils import Pipeline, Salt, FileEncoder
from encoding.text.transposition import RailFenceCipher, ColumnarTranspositionCipher
from encoding.text.substitution import CaesarCipher, AtbashCipher, AffineCipher, VigenereCipher
from tqdm import tqdm

class TestPipeline(unittest.TestCase):
    def test_encode_without_salt(self):
        pipeline = Pipeline([
            (CaesarCipher(), 'caesar_cipher'),
            (RailFenceCipher(), 'rail_cipher'),
            (VigenereCipher(), 'vigenere_cipher')
        ])

        raw_text = "This is an encoding module."
        enc_text = pipeline.encode(text=raw_text)
        dec_text = pipeline.decode(text=enc_text)

        self.assertEqual(raw_text, dec_text)

    def test_encode_with_salt(self):
        pipeline = Pipeline([
            (Salt(), 'salt'),
            (CaesarCipher(), 'caesar_cipher'),
            (RailFenceCipher(), 'rail_cipher'),
            (VigenereCipher(), 'vigenere_cipher')
        ])

        raw_text = "This is an encoding module."
        enc_text = pipeline.encode(text=raw_text)
        dec_text = pipeline.decode(text=enc_text)

        self.assertEqual(raw_text, dec_text)

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


if __name__ == '__main__':
    unittest.main()
