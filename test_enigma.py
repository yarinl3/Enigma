from enigma import *


def test_fix_offset():
    assert fix_offset('c', 4) == 6


def test_encrypt():
    settings = ['par', [3, 1, 2], [('a', 'g'), ('l', 's'), ('d', 'm'), ('n', 'q'), ('w', 'u'), ('z', 'c')]]
    print(encrypt(settings, 'yarin levi', 1))
    assert encrypt(settings, 'yarinlevi', 1) == 'aolvprcrg'
    assert encrypt(settings, 'aolvprcrg', 2) == 'yarinlevi'
