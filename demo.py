"""Демонстрація роботи пакета library (варіант 1: Бібліотека)."""

from __future__ import annotations

from library import (
    AcquisitionSession,
    Book,
    BookNotFound,
    Catalog,
    Year,
    YearDC,
)


def task1_demo() -> None:
    print("=== Завдання 1: незмінний об'єкт-значення Year ===")
    a = Year(1990)
    b = Year(1990)
    c = Year(2005)
    print(f"a = {a!r}, b = {b!r}")
    print(f"a is b -> {a is b}")
    print(f"a == b -> {a == b}")

    years_set = {a, b, c}
    print(f"set({{a, b, c}}) (a==b) -> {years_set}")

    year_map = {a: "перше видання"}
    print(f"словник з a як ключем, доступ через b -> {year_map[b]}")

    print(f"sorted([c, a, Year(1750)]) -> {sorted([c, a, Year(1750)])}")

    try:
        a.value = 2000
    except AttributeError as exc:
        print(f"a.value = 2000 -> перехоплено AttributeError: {exc}")

    print(f"a + b -> {a + b!r}")
    print(f"c - a -> {c - a!r}")
    print(f"a * 2 -> {a * 2!r}")
    print(f"2 * a -> {2 * a!r}")
    try:
        a + 10
    except TypeError as exc:
        print(f"a + 10 (10 не Year) -> перехоплено TypeError: {exc}")

    dc1 = YearDC(1990)
    dc2 = YearDC(1990)
    print(f"YearDC(1990) -> {dc1!r}; dc1 == dc2 -> {dc1 == dc2}; dc1 is dc2 -> {dc1 is dc2}")
    try:
        dc1.value = 2000
    except Exception as exc:  # dataclass(frozen=True) підіймає FrozenInstanceError
        print(f"dc1.value = 2000 -> перехоплено {type(exc).__name__}: {exc}")


def task2_demo() -> None:
    print("\n=== Завдання 2: доменна сутність Book ===")
    book = Book(isbn="978-0-14-044913-6", title="Одіссея", author="Гомер", year=1990, copies=3)
    print(f"Створено: {book!r}")

    try:
        book.year = 1000
    except ValueError as exc:
        print(f"book.year = 1000 -> ValueError: {exc}")

    try:
        Book(isbn="9780140449136", title="X", author="Y", year=3000, copies=1)
    except ValueError as exc:
        print(f"рік з майбутнього у конструкторі -> ValueError: {exc}")

    try:
        book.copies = -1
    except ValueError as exc:
        print(f"book.copies = -1 -> ValueError: {exc}")

    try:
        Book(isbn="9780140449136", title="", author="Y", year=2000, copies=1)
    except ValueError as exc:
        print(f"порожня назва у конструкторі -> ValueError: {exc}")

    try:
        book.author = "   "
    except ValueError as exc:
        print(f"book.author = '   ' -> ValueError: {exc}")

    try:
        book.isbn = "not-an-isbn"
    except ValueError as exc:
        print(f"book.isbn = 'not-an-isbn' -> ValueError: {exc}")

    good = Book.from_dict(
        {"isbn": "9780262033848", "title": "Introduction to Algorithms", "author": "Cormen", "year": 2009, "copies": 5}
    )
    print(f"Book.from_dict (коректний словник) -> {good!r}")

    try:
        Book.from_dict({"isbn": "123", "title": "X", "author": "Y", "year": 2000, "copies": 1})
    except ValueError as exc:
        print(f"Book.from_dict (некоректний isbn) -> ValueError: {exc}")

    print(f"Book.is_valid_isbn('9780140449136') -> {Book.is_valid_isbn('9780140449136')}")
    print(f"Book.is_valid_isbn('abc') -> {Book.is_valid_isbn('abc')}")


def task3_demo() -> None:
    print("\n=== Завдання 3: колекція Catalog ===")
    b1 = Book("9780140449136", "Одіссея", "Гомер", 1990, 3)
    b2 = Book("9780262033848", "Introduction to Algorithms", "Cormen", 2009, 5)
    b3 = Book("9780451524935", "1984", "Джордж Орвелл", 1949, 2)
    b4 = Book("9780060850524", "Дивний новий світ", "Олдос Гакслі", 1932, 1)

    catalog = Catalog([b1, b2, b3, b4])
    print(f"len(catalog) -> {len(catalog)}")
    print(f"catalog[0] -> {catalog[0]}")

    sliced = catalog[0:2]
    print(f"type(catalog[0:2]) -> {type(sliced).__name__}, len -> {len(sliced)}")

    print(f"b3 in catalog -> {b3 in catalog}")
    print(f"'0000000000000' in catalog -> {'0000000000000' in catalog}")

    print("Обхід for:")
    for book in catalog:
        print(f"  {book}")

    print("Посторінковий обхід (по 3), остання сторінка неповна:")
    for page_num, page in enumerate(catalog.pages(3), start=1):
        titles = "; ".join(str(b) for b in page)
        print(f"  сторінка {page_num} ({len(page)} книг(и)): {titles}")

    old_books = catalog(year_to=1950)
    print(f"catalog(year_to=1950) -> {'; '.join(str(b) for b in old_books)}")

    orwell = catalog(author="Джордж Орвелл")
    print(f"catalog(author='Джордж Орвелл') -> {'; '.join(str(b) for b in orwell)}")

    try:
        catalog(publisher="Penguin")
    except TypeError as exc:
        print(f"catalog(publisher=...) -> перехоплено TypeError: {exc}")

    found = catalog.get("9780451524935")
    print(f"catalog.get('9780451524935') -> {found}")
    try:
        catalog.get("0000000000000")
    except BookNotFound as exc:
        print(f"catalog.get(відсутній isbn) -> перехоплено BookNotFound: {exc}")


def task4_demo() -> None:
    print("\n=== Завдання 4: перевантаження операторів ===")
    b1 = Book("9780140449136", "Одіссея", "Гомер", 1990, 3)
    b2 = Book("9780262033848", "Introduction to Algorithms", "Cormen", 2009, 5)
    b3 = Book("9780451524935", "1984", "Джордж Орвелл", 1949, 2)

    cat_a = Catalog([b1])
    cat_b = Catalog([b2])
    cat_c = Catalog([b3, b1])  # b1 навмисно дублюється

    merged = cat_a + cat_b
    print(f"cat_a + cat_b -> len={len(merged)}")

    total = sum([cat_a, cat_b, cat_c])
    print(f"sum([cat_a, cat_b, cat_c]) -> len={len(total)} (дублікат b1 не подвоєно)")

    try:
        cat_a + 5
    except TypeError as exc:
        print(f"cat_a + 5 -> перехоплено TypeError: {exc}")

    y1 = Year(1990)
    y2 = Year(30)
    print(f"y1 + y2 -> {y1 + y2!r}")
    print(f"y1 - y2 -> {y1 - y2!r}")
    print(f"y1 * 2 -> {y1 * 2!r}")
    print(f"3 * y1 -> {3 * y1!r}")

    values = [Year(2005), Year(1450), Year(1990)]
    print(f"min -> {min(values)!r}, max -> {max(values)!r}, sorted -> {sorted(values)!r}")


def task5_demo() -> None:
    print("\n=== Завдання 5: валідаційний декоратор ===")
    catalog = Catalog()
    catalog.add_book_copies(isbn="9780000000002", title="Нова книга", author="Автор", year=2020, copies=2)
    print("add_book_copies з коректними аргументами -> успішно")

    try:
        catalog.add_book_copies(isbn="9780000000003", title="", author="Автор", year=2020, copies=1)
    except ValueError as exc:
        print(f"title='' -> перехоплено ValueError: {exc}")

    try:
        catalog.add_book_copies(isbn="9780000000004", title="Книга", author="Автор", year=2020, copies=-1)
    except ValueError as exc:
        print(f"copies=-1 -> перехоплено ValueError: {exc}")

    try:
        catalog.add_book_copies(isbn="9780000000005", title="Книга", author="   ", year=2020, copies=1)
    except ValueError as exc:
        print(f"author='   ' -> перехоплено ValueError: {exc}")

    print(f"Catalog.add_book_copies.__name__ -> {Catalog.add_book_copies.__name__!r} (а не 'wrapper')")


def task6_demo() -> None:
    print("\n=== Завдання 6: контекстний менеджер AcquisitionSession ===")
    b1 = Book("9780140449136", "Одіссея", "Гомер", 1990, 3)
    catalog = Catalog([b1])

    with AcquisitionSession(catalog) as c:
        c.add_book_copies(isbn="9780000000006", title="Книга А", author="Автор", year=2021, copies=1)
        c.add_book_copies(isbn="9780000000007", title="Книга Б", author="Автор", year=2022, copies=1)
    print(f"Успішний сеанс -> len(catalog) = {len(catalog)} (зміни застосовано)")

    before = len(catalog)
    try:
        with AcquisitionSession(catalog) as c:
            c.add_book_copies(isbn="9780000000008", title="Книга В", author="Автор", year=2023, copies=1)
            c.add_book_copies(isbn="9780000000009", title="Книга Г", author="Автор", year=2023, copies=1)
            raise RuntimeError("Помилка постачання: партію відхилено")
    except RuntimeError as exc:
        print(f"Сеанс перервано винятком: {exc}")
    after = len(catalog)
    print(f"len(catalog) до сеансу == після відкату: {before} == {after} -> {before == after}")


def main() -> None:
    demos = [task1_demo, task2_demo, task3_demo, task4_demo, task5_demo, task6_demo]
    for demo in demos:
        demo()
        print("-" * 70)


if __name__ == "__main__":
    main()
