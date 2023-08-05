from model import *

TEST_SIZE = 4


def test_straight_roads():
    def _test(c, z2):
        b = Board(TEST_SIZE)
        ms = ""
        for m in zip(c if len(c) == TEST_SIZE else c * TEST_SIZE, z2):
            b.force_str(''.join(m), Colors.WHITE)
            ms += ''.join(m) + " "
            if len(ms.split()) < TEST_SIZE:
                try:
                    assert b.road() == False
                    print(ms, "worked!")
                except:
                    print(ms, "did not work")
                    print(b)
                    print(b.road())
                    input()
        try:
            assert b.road() == Colors.WHITE
            print(ms, "worked!")
        except:
            print(ms, "did not work")
            print(b)
            print(b.road())
            input()

    for c in "abcd":
        _test(c, "1234")
    for d in "1234":
         _test("abcd", d * TEST_SIZE)

test_straight_roads()