### String-Encoding

This Python module implements a custom String class that provides various string encoding and transformation utilities, including:
- Base64 Encoding/Decoding
- Byte Pair Encoding/Decoding
- Cyclic Bit and Character Transformations
- Character Frequency Histogram


## Usage
```bash
from String import String

s = String("hello world")

# Base64
encoded = s.base64_encode()
decoded = s.base64_decode()

# Byte Pair Encoding
bpe_encoded = s.byte_pair_encode()
bpe_decoded = s.byte_pair_decode()

# Cyclic Transformations
cyclic_bits = s.cyclic_bits_transform(k=3)
cyclic_chars = s.cyclic_chars_transform(k=2)

# Character Histogram
hist = s.char_histogram()
```


## Requirements
Python 3.x
    Python 3.x

    No external dependencies

License

MIT License
