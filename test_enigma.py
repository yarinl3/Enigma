import enigma


def test_fix_offset():
    test = enigma.fix_offest('c', 4)
    assert test == 7
