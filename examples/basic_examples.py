"""
Example usage of the string-encoding library.
"""

from string_encoding import String

def main():
    print("String-Encoding Examples\n" + "=" * 25)
    
    # Create a test string
    original = String("Hello, World!")
    print(f"Original string: '{original}'")
    
    # Base64 encoding example
    print("\n1. Base64 Encoding")
    print("-" * 20)
    base64_encoded = original.base64()
    print(f"Base64 encoded: '{base64_encoded}'")
    base64_decoded = base64_encoded.decode_base64()
    print(f"Base64 decoded: '{base64_decoded}'")
    print(f"Matches original: {original == base64_decoded}")
    
    # Byte Pair Encoding example
    print("\n2. Byte Pair Encoding")
    print("-" * 20)
    # Using a string with repeating patterns for better BPE demonstration
    repeat_str = String("aaabbbcccaaabbbccc")
    print(f"String with repeating patterns: '{repeat_str}'")
    
    try:
        bpe_encoded = repeat_str.byte_pair_encoding()
        print(f"BPE encoded: '{bpe_encoded}'")
        print(f"BPE rules: {bpe_encoded.rules}")
        bpe_decoded = bpe_encoded.decode_byte_pair()
        print(f"BPE decoded: '{bpe_decoded}'")
        print(f"Matches original: {repeat_str == bpe_decoded}")
    except Exception as e:
        print(f"BPE encoding failed: {e}")
    
    # Cyclic bits transformation
    print("\n3. Cyclic Bits Transformation")
    print("-" * 20)
    shift_amount = 3
    print(f"Shift amount: {shift_amount} bits")
    cyclic_bits = original.cyclic_bits(shift_amount)
    print(f"Cyclic bits transformed: '{cyclic_bits}'")
    cyclic_bits_decoded = cyclic_bits.decode_cyclic_bits(shift_amount)
    print(f"Cyclic bits decoded: '{cyclic_bits_decoded}'")
    print(f"Matches original: {original == cyclic_bits_decoded}")
    
    # Cyclic chars transformation
    print("\n4. Cyclic Characters Transformation")
    print("-" * 20)
    char_shift = 5
    print(f"Shift amount: {char_shift} characters")
    cyclic_chars = original.cyclic_chars(char_shift)
    print(f"Cyclic chars transformed: '{cyclic_chars}'")
    cyclic_chars_decoded = cyclic_chars.decode_cyclic_chars(char_shift)
    print(f"Cyclic chars decoded: '{cyclic_chars_decoded}'")
    print(f"Matches original: {original == cyclic_chars_decoded}")
    
    # Character histogram
    print("\n5. Character Histogram")
    print("-" * 20)
    sample_text = String("Hello 123, WORLD! This is a sample text with UPPER and lower case letters and 456 digits.")
    print(f"Sample text: '{sample_text}'")
    hist = sample_text.histogram_of_chars()
    
    print("Character distribution:")
    total_chars = sum(hist.values())
    for category, count in hist.items():
        percentage = (count / total_chars) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    main()