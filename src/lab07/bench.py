import os
import random
import timeit

from src.lib.io_helpers import write_csv
from src.lab07.search import (linear_search, binary_search,
                              two_sum_brute, two_sum_fast)
from src.lab07.sorting import (bubble_sort, insertion_sort,
                               selection_sort, merge_sort)

OUT = "data/lab07/bench.csv"
QUADRATIC_LIMIT = 10_000  # на больших n квадратичные не запускаем


def t(fn):
    return timeit.timeit(fn, number=1)


def bench_sorts(n):
    rows = []
    data = [random.randint(-10**6, 10**6) for _ in range(n)]
    rows.append(("sort", n, "sorted", t(lambda: sorted(data))))
    rows.append(("sort", n, "merge_sort", t(lambda: merge_sort(data))))
    for name, fn in (("bubble", bubble_sort),
                     ("insertion", insertion_sort),
                     ("selection", selection_sort)):
        if n > QUADRATIC_LIMIT:
            rows.append(("sort", n, name, "> 60"))
        else:
            rows.append(("sort", n, name, t(lambda: fn(data))))
    return rows


def bench_search(n=100_000, queries=10_000):
    data = [random.randint(0, 10**6) for _ in range(n)]
    qs = [random.randint(0, 10**6) for _ in range(queries)]
    rows = []

    def run_linear():
        for q in qs:
            linear_search(data, q)
    rows.append(("search", n, "linear", t(run_linear)))

    holder = {}
    rows.append(("search", n, "sort_for_binary",
                 t(lambda: holder.update(s=sorted(data)))))
    s = holder["s"]

    def run_binary():
        for q in qs:
            binary_search(s, q)
    rows.append(("search", n, "binary", t(run_binary)))
    return rows


def bench_two_sum(n):
    nums = [random.randint(0, 10**9) for _ in range(n)]
    target = nums[-2] + nums[-1]  # ответ гарантированно существует
    return [
        ("two_sum", n, "brute", t(lambda: two_sum_brute(nums, target))),
        ("two_sum", n, "fast", t(lambda: two_sum_fast(nums, target))),
    ]


def to_csv_rows(rows):
    """(task, n, impl, seconds) -> строки для write_csv, секунды как текст."""
    return [
        (task, n, impl, sec if isinstance(sec, str) else f"{sec:.6f}")
        for task, n, impl, sec in rows
    ]


def print_table(rows):
    print(f"{'task':<10}{'n':>10}  {'impl':<18}{'seconds':>12}")
    print("-" * 52)
    for task, n, impl, sec in rows:
        s = sec if isinstance(sec, str) else f"{sec:.6f}"
        print(f"{task:<10}{n:>10}  {impl:<18}{s:>12}")


if __name__ == "__main__":
    random.seed(42)
    rows = []
    for n in (1_000, 10_000, 100_000):
        rows += bench_sorts(n)
    rows += bench_search()
    for n in (1_000, 10_000):
        rows += bench_two_sum(n)

    print_table(rows)

    os.makedirs("data/lab07", exist_ok=True)  # на случай, если write_csv не создаёт папки
    write_csv(to_csv_rows(rows), OUT, header=("task", "n", "impl", "seconds"))