import unittest

from encoding.utils import TextEncoder, Pipeline, Salt, StructuredDataEncoder, TextFileEncoder, JSONFileEncoder
from encoding.ciphers.substitution import CaesarCipher, AtbashCipher, AffineCipher, VigenereCipher
from encoding.ciphers.transposition import RailFenceCipher, ColumnarTranspositionCipher


class CipherTestBase(unittest.TestCase):
    sample_strings = [
        "Hello, World!",
        '12345',
        'Random Characters: !@#$%^&*()_+-=',
        "I'm learning Python.",
        ""
    ]

    def run_cipher_tests(self, encoder):
        for sample_string in self.sample_strings:
            enc_str = encoder.encode(sample_string)
            dec_str = encoder.decode(enc_str)
            self.assertEqual(sample_string, dec_str)


class TestCaesarCipher(CipherTestBase):
    def test_alpha_only_false(self):
        encoder = CaesarCipher(shift=5, alpha_only=False)
        self.run_cipher_tests(encoder)

    def test_alpha_only_true(self):
        encoder = CaesarCipher(shift=5, alpha_only=True)
        self.run_cipher_tests(encoder)


class TestAtbashCipher(CipherTestBase):
    def test_alpha_only_false(self):
        encoder = AtbashCipher(alpha_only=False)
        self.run_cipher_tests(encoder)

    def test_alpha_only_true(self):
        encoder = AtbashCipher(alpha_only=True)
        self.run_cipher_tests(encoder)


class TestAffineCipher(CipherTestBase):
    def test_alpha_only_false(self):
        encoder = AffineCipher(alpha_only=False)
        self.run_cipher_tests(encoder)

    def test_alpha_only_true(self):
        encoder = AffineCipher(alpha_only=True)
        self.run_cipher_tests(encoder)


class TestVigenereCipher(CipherTestBase):
    def test_alpha_only_false(self):
        encoder = VigenereCipher(key="encoding", alpha_only=False)
        self.run_cipher_tests(encoder)

    def test_alpha_only_true(self):
        encoder = VigenereCipher(key="encoding", alpha_only=True)
        self.run_cipher_tests(encoder)


class TestRailCipher(CipherTestBase):
    def test_rails_2(self):
        encoder = RailFenceCipher(rails=2)
        self.run_cipher_tests(encoder)

    def test_rails_10(self):
        encoder = RailFenceCipher(rails=10)
        self.run_cipher_tests(encoder)


class TestCTC(CipherTestBase):
    def test_ctc_key1(self):
        encoder = ColumnarTranspositionCipher()
        self.run_cipher_tests(encoder)

    def test_ctc_key2(self):
        encoder = ColumnarTranspositionCipher(key="world")
        self.run_cipher_tests(encoder)


if __name__ == '__main__':
    unittest.main()
