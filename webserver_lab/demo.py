from dataclasses import FrozenInstanceError
from itertools import islice
from pathlib import Path

from src.webserver.pipeline import (
    parse, normalize, keep, aggregate, process, pipeline, pipeline_comprehension,
    DEFAULT_THRESHOLD,
)
from src.webserver.model import to_record, bump_bytes, rename_path
from src.webserver.hof import (
    compose, pipe, normalize_pipe, normalize_via_loop,
    make_predicate, make_running_total, classify_bytes,
    to_km, to_miles, make_keep_partial, curry3, curried_predicate,
)
from src.webserver.lazy import g_normalize, g_keep, lazy_pipeline, record_stream, take, drop
from src.webserver.recursion import total
from src.webserver.calculator import Num, Neg, Add, Sub, Mul, Div, Pow, Sqrt, Sum, evaluate

DATA_PATH = Path(__file__).parent / "data" / "webserver.txt"


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------------
def demo_task1(lines: list[str]) -> None:
    section("Завдання 1: чисті функції (parse / process)")
    res1 = process(lines, now=1000.0)
    res2 = process(lines, now=1000.0)
    print("res1 == res2 (детермінованість):", res1 == res2)
    print("Кількість помилок (errors):", res1.errors)
    print("Кількість валідних записів:", len(res1.records))
    print("Перший валідний запис:", res1.records[0])


# ---------------------------------------------------------------------------
def demo_task2(lines: list[str]) -> None:
    section("Завдання 2: незмінний Record")
    res = process(lines, now=2000.0)
    rec = to_record(res.records[0])
    print("Record:", rec)

    try:
        rec.bytes = 999  # type: ignore[misc]
    except FrozenInstanceError as e:
        print("Спроба мутації підняла FrozenInstanceError:", e)

    new_rec = bump_bytes(rec, 100)
    print("Новий Record (bump_bytes +100):", new_rec)
    print("Вхідний rec не змінився:", rec)

    renamed = rename_path(rec, "/changed")
    print("Новий Record (rename_path):", renamed)

    record_set = {rec, new_rec}
    record_dict = {rec: "перший запис"}
    print("Record у set:", len(record_set), "елементів; у dict як ключ:", record_dict[rec])

    from dataclasses import dataclass as _dc

    @_dc
    class MutableRecord:
        x: int

    try:
        _ = {MutableRecord(1)}
        print("Звичайний dataclass додався в set (неочікувано)")
    except TypeError as e:
        print("Звичайний (не frozen) dataclass не хешується:", e)


# ---------------------------------------------------------------------------
def demo_task3(lines: list[str]) -> None:
    section("Завдання 3: ФВП та замикання")

    f = lambda n: n + 1
    g = lambda n: n * 2
    h = lambda n: n - 3
    value = 10
    print("compose(f,g,h)(10) == f(g(h(10))):",
          compose(f, g, h)(value) == f(g(h(value))), "->", compose(f, g, h)(value))
    print("pipe(f,g,h)(10) == h(g(f(10))):",
          pipe(f, g, h)(value) == h(g(f(value))), "->", pipe(f, g, h)(value))

    raw = parse(lines[0])
    print("normalize_pipe(raw) :", normalize_pipe(raw))
    print("normalize_via_loop(raw) == normalize_pipe(raw):",
          normalize_via_loop(raw) == normalize_pipe(raw))

    keep_ge = make_predicate("bytes", "ge", DEFAULT_THRESHOLD)
    is_root = make_predicate("path", "eq", "/index.html")
    print("make_predicate ge(bytes,5) на normalize(raw):", keep_ge(normalize(raw)))
    print("make_predicate eq(path,'/index.html'):", is_root(normalize(raw)))

    counter1 = make_running_total()
    counter2 = make_running_total()
    print("counter1: 3,4,5 ->", counter1(3), counter1(4), counter1(5))
    print("counter2 (незалежний): 100 ->", counter2(100))

    normalized_all = [normalize(r) for r in map(parse, lines) if r is not None]
    selected = [r for r in normalized_all if keep(r)]
    running = make_running_total()
    running_result = 0
    for r in selected:
        running_result = running(r["bytes"])
    agg = aggregate(selected)
    print("Сума через make_running_total:", running_result)
    print("Сума значень словника агрегації:", sum(agg.values()))
    print("Збігаються:", running_result == sum(agg.values()))

    print("Класифікація bytes для кількох записів:")
    for r in normalized_all[:5]:
        print(f"  {r['path']!r} bytes={r['bytes']} -> {classify_bytes(r)}")


# ---------------------------------------------------------------------------
def demo_task4(lines: list[str]) -> None:
    section("Завдання 4: конвеєр map/filter/reduce vs спискові включення")
    result_a = pipeline(lines)
    result_b = pipeline_comprehension(lines)
    print("Спосіб A (map/filter/reduce):", result_a)
    print("Спосіб B (спискові включення):", result_b)
    print("Способи дають однаковий словник:", result_a == result_b)
    print("На порожньому вході:", pipeline([]))


# ---------------------------------------------------------------------------
def demo_task5(lines: list[str]) -> None:
    section("Завдання 5: partial та каррирування")
    print("to_km(100) =", to_km(100), " to_miles(100) =", to_miles(100))
    print("to_km(100) != to_miles(100):", to_km(100) != to_miles(100))

    f = lambda a, b, c: a + b * c
    curried = curry3(f)
    print("curry3(f)(1)(2)(3) == f(1,2,3):", curried(1)(2)(3) == f(1, 2, 3))
    print("curry3(f)(1) — це функція:", callable(curried(1)))

    keep_partial = make_keep_partial("bytes", "ge")(DEFAULT_THRESHOLD)
    keep_curried = curried_predicate("bytes")("ge")(DEFAULT_THRESHOLD)

    normalized_all = [normalize(r) for r in map(parse, lines) if r is not None]

    baseline_agg = pipeline(lines)
    agg_via_partial = aggregate(r for r in normalized_all if keep_partial(r))
    agg_via_curried = aggregate(r for r in normalized_all if keep_curried(r))
    print("Агрегація з keep (завд. 4):        ", baseline_agg)
    print("Та сама агрегація з partial-keep:  ", agg_via_partial)
    print("Та сама агрегація з curried-keep:  ", agg_via_curried)
    print("partial-предикат у конвеєрі дає той самий результат:", baseline_agg == agg_via_partial)
    print("каррируваний предикат у конвеєрі дає той самий результат:", baseline_agg == agg_via_curried)


# ---------------------------------------------------------------------------
def demo_task6(data_path: Path) -> None:
    section("Завдання 6: ліниві обчислення")

    with data_path.open(encoding="utf-8") as f:
        eager = pipeline(f.read().splitlines())

    with data_path.open(encoding="utf-8") as f:
        lazy_selected = list(lazy_pipeline(f))
    lazy_agg = aggregate(lazy_selected)
    print("Генераторний конвеєр (лінивий, з файлу) == звичайний конвеєр (завд. 4):",
          eager == lazy_agg)

    print("islice(record_stream(), 5):")
    for rec in islice(record_stream(), 5):
        print("  ", rec)

    finite_from_infinite = list(g_keep(g_normalize(islice(record_stream(), 50))))
    print("Перші 3 з відфільтрованого нескінченного потоку:", finite_from_infinite[:3])

    print("take(3, range(10)) ->", list(take(3, range(10))))
    print("drop(3, range(6)) ->", list(drop(3, range(6))))

    gen = take(3, range(5))
    list(gen)
    print("Повторний обхід вичерпаного генератора:", list(gen))


# ---------------------------------------------------------------------------
def demo_recursion(lines: list[str]) -> None:
    section("Рекурсивний підсумок total() (контрольне запитання 8)")
    normalized_all = [normalize(r) for r in map(parse, lines) if r is not None]
    selected = tuple(r for r in normalized_all if keep(r))
    print("total(selected) =", total(selected))
    print("== sum(agg.values()):", total(selected) == sum(aggregate(selected).values()))
    print("total(()) — база рекурсії:", total(()))


# ---------------------------------------------------------------------------
def demo_task7() -> None:
    section("Завдання 7: калькулятор виразів (match/case)")
    examples = [
        ("(2 + 3) * 4", Mul(Add(Num(2), Num(3)), Num(4))),
        ("(10 - 4) * 2", Mul(Sub(Num(10), Num(4)), Num(2))),
        ("Neg(5) + Num(0)", Add(Neg(Num(5)), Num(0))),
        ("Sum([1,2,3])", Sum((Num(1), Num(2), Num(3)))),
        ("Sum([]) (порожня)", Sum(())),
        ("2 ** 10 (невід'ємний)", Pow(Num(2), 10)),
        ("2 ** -1 (від'ємний)", Pow(Num(2), -1)),
        ("Sqrt(16)", Sqrt(Num(16))),
        ("Sqrt(-4)", Sqrt(Num(-4))),
        ("10 / 0", Div(Num(10), Num(0))),
        ("невідомий вузол", "not_an_expr"),
    ]
    for label, expr in examples:
        try:
            print(f"{label:28s} -> {evaluate(expr)}")
        except ValueError as e:
            print(f"{label:28s} -> ValueError: {e}")


# ---------------------------------------------------------------------------
def main() -> None:
    lines = DATA_PATH.read_text(encoding="utf-8").splitlines()

    demo_task1(lines)
    demo_task2(lines)
    demo_task3(lines)
    demo_task4(lines)
    demo_task5(lines)
    demo_task6(DATA_PATH)
    demo_recursion(lines)
    demo_task7()


if __name__ == "__main__":
    main()
