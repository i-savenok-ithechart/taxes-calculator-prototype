from common.utils import InfinityLimit


def test_compare_infinity_limit():
    assert InfinityLimit() > 999
    assert InfinityLimit() >= 999
    assert not InfinityLimit() == 999
    assert not InfinityLimit() < 999
    assert not InfinityLimit() <= 999


def test_compare_infinity_limit_with_infinity_limit():
    assert not InfinityLimit() > InfinityLimit()
    assert InfinityLimit() >= InfinityLimit()
    assert InfinityLimit() == InfinityLimit()
    assert not InfinityLimit() < InfinityLimit()
    assert InfinityLimit() <= InfinityLimit()
