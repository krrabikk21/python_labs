import random
from src.lab07.search import (linear_search, binary_search,
                              two_sum_brute, two_sum_fast)
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

COUNT = 0  # сколько проверок выполнено


def _rand_list(lo=-100, hi=100, max_n=50):
    n = random.randint(0, max_n)
    return [random.randint(lo, hi) for _ in range(n)]


def check_sorting(fn, trials=100):
    global COUNT
    for _ in range(trials):
        nums = _rand_list()
        original = list(nums)
        result = fn(nums)
        assert result == sorted(nums), f"{fn.__name__} ошиблась на {original}: {result}"
        assert nums == original, f"{fn.__name__} изменила исходный список {original}"
        COUNT += 1


def check_search(trials=100):
    global COUNT
    for _ in range(trials):
        nums = _rand_list()
        x = random.randint(-100, 100)
        try:
            expected = nums.index(x)
        except ValueError:
            expected = -1
        got = linear_search(nums, x)
        assert got == expected, f"linear_search({nums}, {x}) = {got}, ожидалось {expected}"

        s = sorted(nums)
        queries = [x]
        if s:
            queries += [s[0], s[-1], s[len(s) // 2]]
        for q in queries:
            idx = binary_search(s, q)
            if q in s:
                assert idx != -1 and s[idx] == q, f"binary_search({s}, {q}) = {idx}"
            else:
                assert idx == -1, f"binary_search({s}, {q}) = {idx}, ожидалось -1"
        COUNT += 1
    # граничные случаи
    assert binary_search([], 5) == -1
    assert binary_search([5], 5) == 0
    assert binary_search([5], 4) == -1
    assert binary_search([1, 2], 2) == 1
    assert binary_search([1, 2], 1) == 0
    COUNT += 1


def _valid(nums, target, pair):
    i, j = pair
    return 0 <= i < j < len(nums) and nums[i] + nums[j] == target


def check_two_sum(trials=100):
    global COUNT
    for _ in range(trials):
        nums = _rand_list(-20, 20, 15)
        target = random.randint(-40, 40)
        a = two_sum_brute(nums, target)
        b = two_sum_fast(nums, target)
        assert (a is None) == (b is None), \
            f"two_sum разошлись на {nums}, target={target}: brute={a}, fast={b}"
        if a is not None:
            assert _valid(nums, target, a), f"brute неверна: {nums}, {target}, {a}"
            assert _valid(nums, target, b), f"fast неверна: {nums}, {target}, {b}"
        COUNT += 1


if __name__ == "__main__":
    random.seed(42)
    for fn in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn)
    check_search()
    check_two_sum()
    print(f"OK: {COUNT} проверок")