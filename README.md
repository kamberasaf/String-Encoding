# String-Encoding

A custom Python string class with advanced encoding and transformation features.

## Features

- **String Subclass**: Extends Python's built-in string with additional capabilities
- **Base64 Encoding/Decoding**: Convert strings to and from Base64 format
- **Byte Pair Encoding/Decoding**: Compress strings using byte pair encoding algorithm
- **Cyclic Transformations**: 
  - Cyclic bit shifting for binary transformations
  - Cyclic character transformations for ASCII characters
- **Character Histogram**: Analyze character distribution in strings

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/string-encoding.git
cd string-encoding

# Install in development mode
pip install -e .
```

## Usage

```python
from string_encoding import String

# Create a new String instance
s = String("hello world")

# Base64 encoding and decoding
encoded = s.base64()
print(encoded)  # Output: aGVsbG8gd29ybGQ=
decoded = encoded.decode_base64()
print(decoded)  # Output: hello world

# Byte Pair Encoding
bpe = s.byte_pair_encoding()
print(bpe)  # Output will depend on implementation details
print(bpe.rules)  # Show the rules used for encoding
restored = bpe.decode_byte_pair()
print(restored)  # Output: hello world

# Cyclic transformations
shifted_bits = s.cyclic_bits(3)
original_bits = shifted_bits.decode_cyclic_bits(3)

shifted_chars = s.cyclic_chars(5)
original_chars = shifted_chars.decode_cyclic_chars(5)

# Character frequency analysis
hist = s.histogram_of_chars()
print(hist)  # Shows distribution of character types
```

## API Reference

### `String` Class

Inherits from Python's built-in `str` class and adds encoding/decoding methods.

#### Methods

- `base64()` - Encode string to Base64
- `decode_base64()` - Decode a Base64 string
- `byte_pair_encoding()` - Compress using Byte Pair Encoding
- `decode_byte_pair()` - Decompress a Byte Pair encoded string
- `cyclic_bits(num)` - Perform cyclic bit shifting by `num` positions
- `decode_cyclic_bits(num)` - Reverse cyclic bit transformation
- `cyclic_chars(num)` - Perform cyclic character shifting
- `decode_cyclic_chars(num)` - Reverse cyclic character transformation
- `histogram_of_chars()` - Analyze character distribution

## Requirements

- Python 3.6+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
