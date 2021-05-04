import enigma


def test_fix_offset():
    test = enigma.fix_offset('c', 4)
    assert test == 6
