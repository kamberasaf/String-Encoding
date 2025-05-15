"""
String-Encoding - A custom Python string class with advanced encoding/transformation features.

This module provides a String class that extends Python's built-in str type with additional
encoding and transformation capabilities including Base64, Byte Pair Encoding, and cyclic
transformations.
"""

import random

class String(str):
    """
    A string class that extends the built-in str with encoding and transformation capabilities.
    
    This class provides methods for Base64 encoding/decoding, Byte Pair Encoding/decoding,
    cyclic bit and character transformations, and character frequency analysis.
    """
    
    def __new__(cls, str1: str, rules=None):
        return str.__new__(cls, str1)

    def __init__(self, str1: str, rules=None):
        """
        Initialize a new String instance.
        
        Args:
            str1: The string value
            rules: Optional rules for byte pair encoding (used for decoding)
        """
        if rules is None:
            self.rules = []
        else:
            self.rules = rules

    def __add__(self, other):
        """Concatenate with another string and maintain String type."""
        return String(str.__add__(self, other))

    def __radd__(self, other):
        """Right concatenation that maintains String type."""
        return String(str.__add__(other, self))

    def __mul__(self, other):
        """Multiply string and maintain String type."""
        return String(str.__mul__(self, other))

    def __rmul__(self, other):
        """Right multiply and maintain String type."""
        return String(str.__rmul__(self, other))

    def __getitem__(self, index):
        """Get item access that maintains String type."""
        return String(str.__getitem__(self, index))

    def __iter__(self):
        """Iterator that yields String objects instead of str."""
        k = [String(x) for x in str.__iter__(self)]
        for y in k:
            yield y

    def base64(self) -> 'String':
        """
        Encode the String to a base64 string.
        
        Returns:
            A new String instance with the encoded value.
        """
        try:
            ascii = str_2_asci_trans(self)
            if len(ascii) == 0:
                raise AttributeError
            bin_8 = ascii_2_bin_trans(ascii, 8)
        except AttributeError:
            print(f'<{self}> is not possible for base 64 encoding')
            return String(self)
            
        bit6 = turn_to_6_or_8_bits(bin_8, 6)
        new_asci = ascii_2_bin_trans(bit6)
        str_b64 = ascii_2_base64_trans(new_asci)
        return String(str_b64)

    def decode_base64(self) -> 'String':
        """
        Decode the String from base64 to its original form.
        
        Returns:
            A new String instance with the decoded value.
            
        Raises:
            Base64DecodeError: If the string cannot be decoded with base64
        """
        scrunched = ''.join(i for i in self if ord(i) not in priority()[5] and i not in '=')
        str_b64 = ascii_2_base64_trans(scrunched)
        
        if str_b64 is None or len(scrunched) % 4 == 1:
            raise Base64DecodeError(self, 'cannot be decode with base 64')
            
        b64_bin = ascii_2_bin_trans(str_b64, 6)
        full = ''.join(e for e in b64_bin)
        split_strings = []
        
        for index in range(0, len(full), 8):
            split_strings.append(full[index: index + 8])
            
        if len(split_strings[-1]) < 8:
            del split_strings[-1]
            
        asci = ascii_2_bin_trans(split_strings)
        f_str = str_2_asci_trans(asci)
        
        for k in f_str:
            if not (0 <= ord(k) <= 127):
                raise Base64DecodeError(self, 'cannot be decode with base 64')
                
        return String(f_str)

    def byte_pair_encoding(self) -> 'String':
        """
        Encode the String using byte pair encoding compression.
        
        Returns:
            A new String instance with the encoded value and compression rules.
            
        Raises:
            BytePairError: If the string cannot be compressed with byte pair encoding
        """
        str1 = self * 1
        prio = priority()
        valid_groups = valid_gp(group_name(str1))
        counter = count_pairs(str1)
        
        if valid_groups == [] or len(counter) == 0:
            raise BytePairError(self, "can't be used for byte pair encoding.")
            
        rules = []
        s = max(counter.items(), key=lambda x: x[1])
        
        while s[1] > 1:
            try:
                rules.extend([f'{chr(prio[valid_groups[0] - 1][0])} = {s[0]}'])
                str1 = str1.replace(s[0], chr(prio[valid_groups[0] - 1][0]))
                prio[valid_groups[0] - 1].pop(0)
                
                if not prio[valid_groups[0] - 1]:
                    prio.pop(prio.index(prio[valid_groups[0] - 1]))
                    valid_groups.pop(0)
                    if len(valid_groups) == 0:
                        raise BytePairError
                        
                counter = count_pairs(str1)
                s = max(counter.items(), key=lambda x: x[1])
            except BytePairError:
                raise BytePairError(self, "can't be used for byte pair encoding.")
                
        return String(str1, rules)

    def decode_byte_pair(self) -> 'String':
        """
        Decode a byte pair encoded String back to its original form.
        
        Returns:
            A new String instance with the decoded value.
            
        Raises:
            BytePairDecodeError: If the string cannot be decoded
        """
        a = bool(self.rules)  # checks for an empty rules list.
        b = [i for i in self if not (0 <= ord(i) <= 255)]
        
        if len(b) != 0 or not a:
            raise BytePairDecodeError(self, "can't be used for byte pair decoding")
            
        try:
            copy_rules = self.rules[::-1]
            for index, item in enumerate(copy_rules):
                self = self.replace(copy_rules[index].replace(' ', '').split('=')[0],
                                   copy_rules[index].replace(' ', '').split('=')[1])
        except (TypeError, AttributeError, IndexError):
            raise BytePairDecodeError(self, "can't be used for byte pair decoding")

        return String(self)

    def cyclic_bits(self, num: int) -> 'String':
        """
        Encode the String using cyclic bit shifting.
        
        Args:
            num: Number of bit positions to shift
            
        Returns:
            A new String instance with bits shifted cyclically
        """
        ascii = str_2_asci_trans(self)
        bin_8 = ascii_2_bin_trans(ascii, 8)
        try:
            skunk = "".join(e for e in bin_8)
        except TypeError:
            return None
            
        num = num % len(skunk)
        i = 1
        if num < 0:
            i = -1
            
        for k in range(0, num, i):
            skunk = skunk[1:] + skunk[0]
            
        bit8 = turn_to_6_or_8_bits(skunk, 8)
        asci = ascii_2_bin_trans(bit8)
        new_str = "".join([chr(i) for i in asci])
        
        return String(new_str)

    def decode_cyclic_bits(self, num: int) -> 'String':
        """
        Decode a string that was encoded with cyclic_bits.
        
        Args:
            num: The same number used during encoding
            
        Returns:
            A new String instance with the original value
        """
        ascii = str_2_asci_trans(self)
        bin_8 = ascii_2_bin_trans(ascii, 8)
        skunk = "".join(e for e in bin_8)
        
        num = num % len(skunk)
        i = 1
        if num < 0:
            i = -1
            
        for k in range(0, num, i):
            skunk = skunk[-1] + skunk[:-1]
            
        bit8 = turn_to_6_or_8_bits(skunk, 8)
        asci = ascii_2_bin_trans(bit8)
        old_str = "".join([chr(i) for i in asci])
        
        return String(old_str)

    def cyclic_chars(self, num: int) -> 'String':
        """
        Transform the String using cyclic character shifting.
        
        Args:
            num: Number of ASCII positions to shift each character
            
        Returns:
            A new String instance with characters shifted
            
        Raises:
            CyclicCharsError: If the string contains invalid characters
        """
        ascii = str_2_asci_trans(self)
        new_ascii = []
        
        for i in ascii[:]:
            if i < 32 or 126 < i:
                raise CyclicCharsError(self, f"can't use cyclic chars with number {num}")
                
            num = valid_num_check(num)
            if not num and num != 0:
                return None
                
            s = 1
            if num < 0:
                s = -1
                
            b = (num * s) % 95
            b *= s
            i += b
            
            if i > 126:
                i = i - 95
            if i < 32:
                i = i + 95
                
            new_ascii.append(i)
            
        try:
            new_str = "".join(chr(i) for i in new_ascii)
            return String(new_str)
        except (ValueError, TypeError):
            raise CyclicCharsError(self, f"can't use cyclic chars with number {num}")

    def decode_cyclic_chars(self, num: int) -> 'String':
        """
        Decode a string that was encoded with cyclic_chars.
        
        Args:
            num: The same number used during encoding
            
        Returns:
            A new String instance with the original value
            
        Raises:
            CyclicCharsDecodeError: If the string contains invalid characters
        """
        ascii = str_2_asci_trans(self)
        new_ascii = []
        
        for i in ascii[:]:  # 32-126
            if i < 32 or 126 < i:
                raise CyclicCharsDecodeError(self, f"can't use decode cyclic chars with number {num}")
                
            num = valid_num_check(num)
            if not num and num != 0:
                return None
                
            s = 1
            if num < 0:
                s = -1
                
            b = (num * s) % 95
            b *= s
            i -= b
            
            if i < 32:
                i = i + 95
            if i > 126:
                i = i - 95
                
            new_ascii.append(i)
            
        try:
            old_str = "".join(chr(i) for i in new_ascii)
            return String(old_str)
        except (ValueError, TypeError):
            raise CyclicCharsDecodeError(self, f"can't use decode cyclic chars with number {num}")

    def histogram_of_chars(self) -> dict:
        """
        Calculate the histogram of character types in the String.
        
        The bins are: "control code", "digits", "upper", "lower",
        "other printable", and "higher than 128".
        
        Returns:
            A dictionary with character categories as keys and counts as values
        """
        histogram = {
            'control code': 0,
            'digits': 0,
            'upper': 0,
            'lower': 0,
            'other printable': 0,
            'higher than 128': 0
        }
        
        for i in self:
            if ord(i) in priority()[0] + [32]:
                histogram['other printable'] += 1
            if ord(i) in priority()[1]:
                histogram['digits'] += 1
            if ord(i) in priority()[2]:
                histogram['upper'] += 1
            if ord(i) in priority()[3]:
                histogram['lower'] += 1
            if ord(i) in priority()[4]:
                histogram['higher than 128'] += 1
            if ord(i) in priority()[5]:
                histogram['control code'] += 1
                
        return histogram


# Base64 translation dictionary
translate_dict = {
    'A': 0, 'Q': 16, 'g': 32, 'w': 48,
    'B': 1, 'R': 17, 'h': 33, 'x': 49,
    'C': 2, 'S': 18, 'i': 34, 'y': 50,
    'D': 3, 'T': 19, 'j': 35, 'z': 51,
    'E': 4, 'U': 20, 'k': 36, '0': 52,
    'F': 5, 'V': 21, 'l': 37, '1': 53,
    'G': 6, 'W': 22, 'm': 38, '2': 54,
    'H': 7, 'X': 23, 'n': 39, '3': 55,
    'I': 8, 'Y': 24, 'o': 40, '4': 56,
    'J': 9, 'Z': 25, 'p': 41, '5': 57,
    'K': 10, 'a': 26, 'q': 42, '6': 58,
    'L': 11, 'b': 27, 'r': 43, '7': 59,
    'M': 12, 'c': 28, 's': 44, '8': 60,
    'N': 13, 'd': 29, 't': 45, '9': 61,
    'O': 14, 'e': 30, 'u': 46, '+': 62,
    'P': 15, 'f': 31, 'v': 47, '/': 63
}


class Base64Error(Exception):
    """Base exception class for encoding/decoding errors."""
    def __init__(self, str, message):
        self.str = str
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"<{self.str}> {self.message}"


class Base64DecodeError(Base64Error):
    """Exception raised when base64 decoding fails."""
    pass


class CyclicCharsError(Base64Error):
    """Exception raised when cyclic character transformation fails."""
    pass


class CyclicCharsDecodeError(Base64Error):
    """Exception raised when cyclic character decoding fails."""
    pass


class BytePairError(Base64Error):
    """Exception raised when byte pair encoding fails."""
    pass


class BytePairDecodeError(Base64Error):
    """Exception raised when byte pair decoding fails."""
    pass


def valid_num_check(word: int, num=0) -> float or bool:
    """
    Validate that a number is an integer.
    
    Args:
        word: The number to validate
        num: Optional default value
        
    Returns:
        The integer value or False if invalid
    """
    try:
        if '.' in str(word):
            for s in set(str(word).split('.')[1:]):
                if s != '0':
                    print('\nPlease enter a valid number.\n')
                    return False
        word = float(word)
        word = int(word)
    except (ValueError, TypeError):
        print('\nPlease enter a valid number.\n')
        return False
    return word


def priority():
    """
    Define ASCII character priority groups for encoding/decoding.
    
    Returns:
        A list of lists, each containing ASCII values for a character group
    """
    priority = [
        [i for i in range(33, 48)] + [i for i in range(58, 65)] + [i for i in range(91, 97)] + [124, 125, 126],
        [i for i in range(48, 58)],
        [i for i in range(65, 91)],
        [i for i in range(97, 123)],
        [i for i in range(128, 256)],
        [i for i in range(32)] + [127]
    ]
    return priority


def valid_gp(gn):
    """
    Determine valid groups for byte pair encoding based on character groups.
    
    Args:
        gn: List of group numbers present in the string
        
    Returns:
        List of valid group numbers for encoding
    """
    numbers = [1, 2, 3, 4]
    if 1 in gn:
        numbers.remove(1)
    if 2 in gn:
        numbers.remove(2)
    if 3 in gn:
        numbers.remove(3)
    if 4 in gn:
        numbers.remove(4)
    return numbers


def group_name(str5):
    """
    Determine which character groups are present in a string.
    
    Args:
        str5: The string to analyze
        
    Returns:
        List of unique group numbers found in the string
    """
    gn = []
    try:
        for i in str5:
            if ord(i) in priority()[0]:
                gn.append(1)
                continue
            elif ord(i) in priority()[1]:
                gn.append(2)
                continue
            elif ord(i) in priority()[2]:
                gn.append(3)
                continue
            gn.append(4)
        return list(set(gn))
    except TypeError:
        pass


def count_pairs(b: str) -> dict:
    """
    Count adjacent character pairs in a string.
    
    Args:
        b: The string to analyze
        
    Returns:
        Dictionary with character pairs as keys and counts as values
        
    Raises:
        BytePairError: If the string contains invalid characters
    """
    dict_1 = {}
    skipped = False
    a = [i for i in b if not (0 <= ord(i) <= 255)]
    
    if len(a) != 0:
        raise BytePairError(b, "can't be used for byte pair encoding.")
        
    for i in range(len(list(b))):
        try:
            a_n = b[i] + b[i + 1]
            if a_n not in dict_1.keys():
                dict_1[a_n] = 1
                continue
                
            a_n_1 = b[i - 1] + b[i]
            if a_n == a_n_1 and not skipped:
                skipped = True
                continue
                
            dict_1[a_n] += 1
            skipped = False
            
        except IndexError:
            pass
            
    return dict_1


def turn_to_6_or_8_bits(chunk: list, bits: int) -> list:
    """
    Convert a list of binary strings to fixed-width bit strings.
    
    Args:
        chunk: List of binary strings
        bits: Target bit width (6 or 8)
        
    Returns:
        List of fixed-width bit strings
    """
    try:
        full = ''.join(e for e in chunk)
        split_strings = []
        
        for index in range(0, len(full), bits):
            split_strings.append(full[index: index + bits])
            
        if len(split_strings[-1]) != bits:
            split_strings[-1] = split_strings[-1].ljust(bits, '0')
            
        if bits == 8 and split_strings[-1] == '0' * 8:
            del split_strings[-1]
            
        return split_strings
    except TypeError:
        pass


def str_2_asci_trans(b: str or int) -> list or str:
    """
    Convert between string and ASCII values.
    
    Args:
        b: String to convert to ASCII, or list of ASCII values to convert to string
        
    Returns:
        List of ASCII values if input is a string, 
        or a string if input is a list of ASCII values
    """
    try:
        if isinstance(b, str):
            return [ord(i) for i in b]  # str to ascii
        if isinstance(b[0], int):  # ascii to str
            return "".join([chr(x) for x in b])
    except (IndexError, TypeError):
        pass


def ascii_2_bin_trans(b: list, num=None) -> list:
    """
    Convert between ASCII values and binary strings.
    
    Args:
        b: List of ASCII values or binary strings
        num: Target bit width (optional)
        
    Returns:
        List of binary strings if input is ASCII values,
        or list of ASCII values if input is binary strings
    """
    try:
        if isinstance(b[0], str):
            return [int(k, 2) for k in b]
            
        a = [bin(int(i)).replace("b", "") for i in b]
        
        for s in a[:]:
            if len(s) < num:
                k = s.rjust(num, '0')
                a.insert(a.index(s), k)
                a.pop(a.index(s))
            elif len(s) != num:
                k = s[-num:]
                a.insert(a.index(s), k)
                a.pop(a.index(s))
                
        return a
    except (TypeError, IndexError):
        pass


def ascii_2_base64_trans(b: list or str):
    """
    Convert between ASCII values and base64 characters.
    
    Args:
        b: List of ASCII values or string of base64 characters
        
    Returns:
        String of base64 characters if input is ASCII values,
        or list of ASCII values if input is base64 characters
    """
    try:
        if isinstance(b[0], int):
            return ''.join(k for v in b for k, s in translate_dict.items() if v == s)
        return [translate_dict[val] for val in b]
    except (KeyError, IndexError, TypeError):
        return None


def generate_random_string(num: int) -> str:
    """
    Generate a random string of specified length.
    
    Args:
        num: Length of the string to generate
        
    Returns:
        Random string with alphanumeric and special characters
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/*-+ ?><:.,/';"
    return ''.join(random.choice(letters) for i in range(num))


if __name__ == '__main__':
    a = String('iaaaiaaiaa', ['avocad=baan'])
    b = a.decode_byte_pair()
    print(a)
    print(a.rules)
    print(b)
    print(b.rules)