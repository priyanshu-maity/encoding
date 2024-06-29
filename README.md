# Encoding Package

## Introduction

The `encoding` package provides a variety of tools for encoding and decoding text using classical and modern ciphers. It includes implementations for various substitution ciphers, transposition ciphers, and utilities for handling structured data and files.

## Table of Contents
1. [Introduction](#introduction)
2. [Contents](#contents)
3. [Features](#features)
   - [Utils](#utils)
   - [Substitution Ciphers](#substitution-ciphers)
   - [Transposition Ciphers](#transposition-ciphers)
4. [Usage](#usage)
5. [Requirements](#requirements)
6. [Installation](#installation)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

## Introduction

This encoding module provides a collection of classes for various text encoding and decoding techniques, including substitution and transposition ciphers. It's designed to be flexible, extensible, and easy to use.

## Contents

The module consists of the following files:

1. `utils.py`: Contains utility classes and functions for text encoding and decoding.
2. `ciphers/substitution.py`: Implements various substitution ciphers.
3. `ciphers/transposition.py`: Implements transposition ciphers.

## Features

### Utils

- `TextEncoder`: A metaclass ensuring proper implementation of encode and decode methods.
- `Pipeline`: Manages sequences of encoders for chained encoding/decoding operations.
- `Salt`: Adds and removes random characters to/from text.
- `StructuredDataEncoder`: Handles encoding and decoding of structured data (lists, tuples, dicts, sets).
- `TextFileEncoder`: Encodes and decodes text files.
- `JSONFileEncoder`: Encodes and decodes JSON files.

### Substitution Ciphers

- `CaesarCipher`:
  - Attributes:
    - `shift` (int): The number of positions to shift each character.
    - `alpha_only` (bool): Whether to encode only alphabetic characters.
  
  [To learn about Caesar Cipher, click here!](https://github.com/cup-of-logic/encoding)
<br><br>

- `AtbashCipher`:
  - Attributes:
    - `alpha_only` (bool): Whether to encode only alphabetic characters.
    
  [To learn about Atbash Cipher, click here!](https://github.com/cup-of-logic/encoding)
<br><br>
    
- `AffineCipher`:
  - Attributes:
    - `key_a` (int): The multiplicative key.
    - `key_b` (int): The additive key.
    - `alpha_only` (bool): Whether to encode only alphabetic characters.

  [To learn about Affine Cipher, click here!](https://github.com/cup-of-logic/encoding)
<br><br>

- `VigenereCipher`:
  - Attributes:
    - `key` (str): The key to use for the cipher.
    - `alpha_only` (bool): Whether to encode only alphabetic characters.
    - `final_key` (str): The repeated key to match the length of the text.

  [To learn about Vigenère Cipher, click here!](https://github.com/cup-of-logic/encoding)
<br><br>

### Transposition Ciphers

- `RailFenceCipher`:
  - Attributes:
    - `rails` (int): The number of rails to use in the cipher.
    - `rf_arr` (ndarray): The array used to store the zig-zag pattern of characters.
  
    - [To learn about Rail Fence Cipher, click here!](https://github.com/cup-of-logic/encoding)
<br><br>

- `ColumnarTranspositionCipher`:
  - Attributes:
    - `key` (str): The key to use for the cipher.
    - `filler` (str): The filler character to use for padding.
    - `txt_arr` (ndarray): The array used to store the characters in columnar order.
    - `order_list` (list): The order of columns based on the key.

  [To learn about Columnar Transposition Cipher, click here!](https://github.com/cup-of-logic/encoding)
<br><br>

## Usage

Here's a basic example of how to use a cipher from this module:

```python
from encoding.ciphers.substitution import CaesarCipher

# Create a Caesar cipher with a shift of 3
caesar = CaesarCipher(shift=3)

# Encode a message
encoded = caesar.encode("Hello, World!")
print(f"Encoded: {encoded}")

# Decode the message
decoded = caesar.decode(encoded)
print(f"Decoded: {decoded}")
```

## Requirements

* Python (>=3.6)
* numpy

## Installation

To use this module, download it from github using the command:

```bash
pip install git+https://github.com/cup-of-logic/encoding.git
```

Or, you can install it directly from PyPI using the command:

```bash
pip install encoding
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Current Contributor(s):
abhineet-bhattacharjee


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Contact

For any questions, feedback, or contributions, please feel free to reach out:

- **Developer:** Priyanshu Maity
- **Email:** priyanshu.maity2006@gmail.com
- **GitHub:** [@cup-of-logic](https://github.com/cup-of-logic)

You can also open an issue in this repository if you encounter any problems or have suggestions for improvements.

Project Link: [encoding](https://github.com/cup-of-logic/encoding)
