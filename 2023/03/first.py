"""
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

import dataclasses
import pathlib
import re
from typing import Iterator


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"


@dataclasses.dataclass
class Point:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash(repr(self))


NUMBER_REGEX = re.compile(r"\d+")


def __find_numbers(content: list[str]) -> Iterator[tuple[Point, Point]]:
    for row, line in enumerate(content):
        for m in NUMBER_REGEX.finditer(line):
            yield Point(row, m.start()), Point(row, m.end() - 1)


def find_numbers(content: list[str]) -> list[tuple[Point, Point]]:
    all_numbers = list(__find_numbers(content))
    # print(all_numbers)
    return all_numbers


def get_size(content: list[str]) -> tuple[int, int]:
    return len(content) - 1, len(content[0]) - 1


def find_frontier(
    p_start: Point, p_end: Point, size: tuple[int, int]
) -> Iterator[Point]:
    max_row, max_col = size
    row = p_start.row
    assert row == p_end.row
    assert p_start.col <= p_end.col

    # print("top")
    if row > 0:
        if p_start.col > 0:
            yield Point(row - 1, p_start.col - 1)
        for col_num in range(p_start.col, p_end.col + 1):
            yield Point(row - 1, col_num)
        if p_end.col < max_col:
            yield Point(row - 1, p_end.col + 1)
    # print("left")
    if p_start.col > 0:
        # first corner already returned
        yield Point(row, p_start.col - 1)
        if row < max_row:
            yield Point(row + 1, p_start.col - 1)
    # print("right")
    if p_end.col < max_col:
        # first corner already returned
        yield Point(row, p_end.col + 1)
        if row < max_row:
            yield Point(row + 1, p_end.col + 1)
    # print("bottom")
    if row < max_row:
        # both corners already returned
        for col_num in range(p_start.col, p_end.col + 1):
            yield Point(row + 1, col_num)


def is_num_valid(content: list[str], num: tuple[Point, Point]) -> bool:
    size = get_size(content)
    for p in find_frontier(num[0], num[1], size):
        cell = content[p.row][p.col]
        if cell not in "0123456789.":
            return True
    return False


def get_num(content: list[str], num: tuple[Point, Point]) -> int:
    p_start, p_end = num
    return int(content[p_start.row][p_start.col : p_end.col + 1])


def main() -> None:
    content = puzzle_file.read_text().splitlines()
    print(
        sum(
            get_num(content, num)
            for num in find_numbers(content)
            if is_num_valid(content, num)
        )
    )


TEST_CASE = [
    "....",
    ".10.",
    "....",
]
TEST_CASE_2 = [
    "....",
    ".12.",
    ".*..",
]
TEST_CASE_3 = [
    "&..",
    ".23",
]


# def assert_set(set1: set[Any], set2: set[Any]) -> None:
#     assert not set1 - set2, set1 - set2
#     assert not set2 - set1, set2 - set1


def test_find_num() -> None:
    test_case = [
        "12.45",
        "..34.",
        "12345",
    ]
    assert find_numbers(test_case) == [
        (Point(0, 0), Point(0, 1)),
        (Point(0, 3), Point(0, 4)),
        (Point(1, 2), Point(1, 3)),
        (Point(2, 0), Point(2, 4)),
    ]
    for num in find_numbers(test_case):
        get_num(test_case, num)


def test_frontier(test_case: list[str], n_dots: int) -> None:
    ((start, end),) = find_numbers(test_case)
    size = get_size(test_case)
    frontier = list(find_frontier(start, end, size))
    for p in frontier:
        assert test_case[p.row][p.col] == "."
    assert len(frontier) == n_dots
    assert len(set(frontier)) == n_dots


if __name__ == "__main__":
    test_find_num()
    test_frontier(TEST_CASE, 10)
    test_frontier(["1.", ".."], 3)
    test_frontier(["...", "..1"], 3)

    assert is_num_valid(TEST_CASE, find_numbers(TEST_CASE)[0]) is False
    assert is_num_valid(TEST_CASE_2, find_numbers(TEST_CASE_2)[0]) is True
    assert is_num_valid(TEST_CASE_3, find_numbers(TEST_CASE_3)[0]) is True
    assert get_num(TEST_CASE, find_numbers(TEST_CASE)[0]) == 10
    assert get_num(TEST_CASE_2, find_numbers(TEST_CASE_2)[0]) == 12
    assert get_num(TEST_CASE_3, find_numbers(TEST_CASE_3)[0]) == 23

    main()
