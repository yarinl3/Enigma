from enigma import *


def test_fix_offset():
    assert fix_offset('c', 4) == 6


def test_encrypt():
    settings = ['par', [3, 1, 2], [('a', 'g'), ('l', 's'), ('d', 'm'), ('n', 'q'), ('w', 'u'), ('z', 'c')]]
    assert encrypt(settings, 'yarinlevi') == 'ictbnujmg'
