import re
import pytest

def cipher(text, shift, encrypt=True):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_text = ''
    for c in text:
        index = alphabet.find(c)
        if index == -1:
            new_text += c
        else:
            new_index = index + shift if encrypt == True else index - shift
            new_index %= len(alphabet)
            new_text += alphabet[new_index:new_index+1]
    return new_text
    
@pytest.mark.parametrize("text, shift, expected", [
    ('a',1,'b'),
    ('b',-1,'a'),
    ('NOPE!',4,'RSTI!'),
    ('L', 3, 'O'),
    ('columbia', 4,'gspyqfme'),
    ('COLUMBIA', 4,'GSPYQFME'),
    ('Columbia university is in Ivy League.', 1, 'Dpmvncjb vojwfstjuz jt jo Jwz Mfbhvf.'),
])  

class TestClass:
    def test_cipher_with_single_word(self, text, shift, expected):
        actual = cipher(text, shift)
        assert actual == expected, 'cipher fails test.'

    def test_cipher_with_negative_shift(self, text, shift, expected):
        if shift < 0:
            actual = cipher(text, shift)
            assert actual == expected, 'cipher fails test with negative shift.'
        
    def test_cipher_with_symbols(self, text, shift, expected):
        if re.findall('[^0-9a-zA-Z]+',text) != []:
                actual = cipher(text, shift)
                assert actual == expected, 'cipher fails test with symbols.'
        