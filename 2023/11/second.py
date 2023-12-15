"""
The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""
import itertools
import pathlib
from typing import Iterator


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"


def find_galaxies(puzzle: list[str]) -> Iterator[tuple[int, int]]:
    for row, line in enumerate(puzzle):
        for col, char in enumerate(line):
            if char == "#":
                yield row, col


def transpose(puzzle: list[str]) -> list[str]:
    return ["".join(line) for line in zip(*puzzle)]


def expand_rows(puzzle: list[str]) -> list[int]:
    return [idx for idx, line in enumerate(puzzle) if "#" not in line]


def expand_cols(puzzle: list[str]) -> list[int]:
    return expand_rows(transpose(puzzle))


def calculate_distance(
    start: tuple[int, int],
    end: tuple[int, int],
    universe: list[str],
    *,
    expanded_rows: list[int],
    expanded_cols: list[int],
    multiplier: int,
) -> int:
    if universe[start[0]][start[1]] != "#":
        raise ValueError(f"Start is not a galaxy: {start}")
    if universe[end[0]][end[1]] != "#":
        raise ValueError(f"End is not a galaxy: {end}")

    extra_rows = sum(
        1
        for idx in range(min(start[0], end[0]) + 1, max(start[0], end[0]))
        if idx in expanded_rows
    )
    extra_cols = sum(
        1
        for idx in range(min(start[1], end[1]) + 1, max(start[1], end[1]))
        if idx in expanded_cols
    )

    res = (
        abs(start[0] - end[0])
        + abs(start[1] - end[1])
        + (extra_rows + extra_cols) * (multiplier - 1)
    )
    # print(f"{start=} {end=} {res=}")
    # print(
    #     f"{extra_rows=} {extra_cols=} {abs(start[0] - end[0])+ abs(start[1] - end[1])=}"
    # )

    return res


def play_game(puzzle: list[str], multiplier: int) -> int:
    expanded_rows = expand_rows(puzzle)
    expanded_cols = expand_cols(puzzle)
    return sum(
        calculate_distance(
            start,
            end,
            puzzle,
            expanded_rows=expanded_rows,
            expanded_cols=expanded_cols,
            multiplier=multiplier,
        )
        for start, end in itertools.combinations(find_galaxies(puzzle), 2)
    )


def test_expand() -> None:
    puzzle = [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#.....",
    ]
    assert len(expand_cols(puzzle)) == 3
    assert len(expand_rows(puzzle)) == 2


def test_calculate_distance() -> None:
    expanded_rows = expand_rows(EXAMPLE)
    expanded_cols = expand_cols(EXAMPLE)
    assert (
        calculate_distance(
            (0, 3),
            (8, 7),
            EXAMPLE,
            expanded_rows=expanded_rows,
            expanded_cols=expanded_cols,
            multiplier=2,
        )
        == 15
    )  # 1  # 7
    assert (
        calculate_distance(
            (2, 0),
            (6, 9),
            EXAMPLE,
            expanded_rows=expanded_rows,
            expanded_cols=expanded_cols,
            multiplier=2,
        )
        == 17
    )
    assert (
        calculate_distance(
            (9, 0),
            (9, 4),
            EXAMPLE,
            expanded_rows=expanded_rows,
            expanded_cols=expanded_cols,
            multiplier=2,
        )
        == 5
    )
    assert (
        calculate_distance(
            (0, 3),
            (1, 7),
            EXAMPLE,
            expanded_rows=expanded_rows,
            expanded_cols=expanded_cols,
            multiplier=2,
        )
        == 6
    )


EXAMPLE = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]


def test_play_game() -> None:
    assert play_game(EXAMPLE, 2) == 374
    assert play_game(EXAMPLE, 10) == 1030
    assert play_game(EXAMPLE, 100) == 8410


def main() -> None:
    puzzle = puzzle_file.read_text().splitlines()
    print(play_game(puzzle, 1000000))


if __name__ == "__main__":
    main()
