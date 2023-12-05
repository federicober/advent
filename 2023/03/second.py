"""
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

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

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
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


def get_num(content: list[str], num: tuple[Point, Point]) -> int:
    p_start, p_end = num
    return int(content[p_start.row][p_start.col : p_end.col + 1])


def create_index(content: list[str]) -> dict[Point, list[tuple[Point, Point]]]:
    size = get_size(content)
    index_dict: dict[Point, list[tuple[Point, Point]]] = {}
    for p in find_numbers(content):
        for frontier_p in find_frontier(*p, size):
            if content[frontier_p.row][frontier_p.col] == "*":
                if frontier_p not in index_dict:
                    index_dict[frontier_p] = []
                index_dict[frontier_p].append(p)
    return index_dict


def main() -> None:
    content = puzzle_file.read_text().splitlines()
    index_dict = create_index(content)
    nums = [
        [get_num(content, point) for point in points]
        for points in index_dict.values()
        if len(points) == 2
    ]
    print(sum(a * b for a, b in nums))


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
TEST_CASE_4 = [
    ".12.",
    ".*..",
    ".23.",
    "....",
]


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


def test_get_num() -> None:
    assert get_num(TEST_CASE, find_numbers(TEST_CASE)[0]) == 10
    assert get_num(TEST_CASE_2, find_numbers(TEST_CASE_2)[0]) == 12
    assert get_num(TEST_CASE_3, find_numbers(TEST_CASE_3)[0]) == 23


def test_get_frontiers() -> None:
    test_frontier(TEST_CASE, 10)
    test_frontier(["1.", ".."], 3)
    test_frontier(["...", "..1"], 3)


if __name__ == "__main__":
    test_find_num()
    test_get_frontiers()
    test_get_num()

    assert create_index(TEST_CASE_4) == {
        Point(1, 1): [(Point(0, 1), Point(0, 2)), (Point(2, 1), Point(2, 2))]
    }

    main()
