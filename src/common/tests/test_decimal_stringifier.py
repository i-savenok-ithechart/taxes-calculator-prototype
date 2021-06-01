from common.decimal import Decimal, to_string


def test_stringify():
    for val, expected in [
        (Decimal(0.11119), '0.1112'),
        (0.11119, '0.1112'),
        ('0.11119', '0.1112'),
        (120, '120.0000'),
    ]:
        assert isinstance(to_string(val), str)
        assert to_string(val) == expected
