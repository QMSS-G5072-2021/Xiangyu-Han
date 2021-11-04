import pytest

def cipher(text, shift, encrypt=True):
    assert isinstance(shift, int), "shift argument should be type int"
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

def test_cipher_with_single_word():
    actual = cipher('a',1)
    expect = 'b'
    assert actual == expect
    
def test_cipher_with_negative_shift():
    actual = cipher('b',-1)
    expect = 'a'
    assert actual == expect

def test_cipher_with_symbols():
    actual = cipher('NOPE!',4)
    expect = 'RSTI!'
    assert actual == expect
    
def test_cipher_with_exception():
    with pytest.raises(AssertionError):
        cipher('d','one')