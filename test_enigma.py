import enigma


def test_fix_offset():
    test = enigma.fix_offset('c', 4)
    assert test == 6


def test_encrypt():
    settings = ['par', [3, 1, 2], [('a', 'g'), ('l', 's'), ('d', 'm'), ('n', 'q'), ('w', 'u'), ('z', 'c')]]
    assert encrypt(settings, '') == ''
    assert encrypt(settings, '   ') == ''
    assert encrypt(settings, '\n') == ''
    assert encrypt(settings, 'yarin levi') == 'ictbnujmg'
