"""
You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

    Between galaxy 1 and galaxy 7: 15
    Between galaxy 3 and galaxy 6: 17
    Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
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


def expand_universe_vertically(puzzle: list[str]) -> list[str]:
    result = []
    for line in puzzle:
        if "#" not in line:
            result.append(line)
        result.append(line)
    return result


def expand_universe(puzzle: list[str]) -> list[str]:
    vert_expanded = expand_universe_vertically(puzzle)
    transposed = transpose(vert_expanded)
    horz_expanded = expand_universe_vertically(transposed)
    return transpose(horz_expanded)


def calculate_distance(
    start: tuple[int, int], end: tuple[int, int], universe: list[str]
) -> int:
    if universe[start[0]][start[1]] != "#":
        raise ValueError(f"Start is not a galaxy: {start}")
    if universe[end[0]][end[1]] != "#":
        raise ValueError(f"End is not a galaxy: {end}")
    res = abs(start[0] - end[0]) + abs(start[1] - end[1])
    # print(f"{start=} {end=} {res=}")
    return res


def play_game(puzzle: list[str]) -> int:
    expanded = expand_universe(puzzle)
    return sum(
        calculate_distance(start, end, expanded)
        for start, end in itertools.combinations(find_galaxies(expanded), 2)
    )


def test_calculate_distance() -> None:
    puzzle = [
        "....#........",
        ".........#...",
        "#............",
        ".............",
        ".............",
        "........#....",
        ".#...........",
        "............#",
        ".............",
        ".............",
        ".........#...",
        "#....#.......",
    ]
    assert calculate_distance((0, 4), (10, 9), puzzle) == 15  # 1  # 7
    assert calculate_distance((2, 0), (7, 12), puzzle) == 17
    assert calculate_distance((11, 0), (11, 5), puzzle) == 5
    assert calculate_distance((0, 4), (1, 9), puzzle) == 6


def test_play_game() -> None:
    assert (
        play_game(
            [
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
        )
        == 374
    )
    assert False


def test_expand_universe() -> None:
    assert expand_universe(
        [
            "#.#",
            "...",
            "#.#",
        ]
    ) == [
        "#..#",
        "....",
        "....",
        "#..#",
    ]
    assert expand_universe(
        [
            "...",
            ".#.",
            "...",
        ]
    ) == [
        ".....",
        ".....",
        "..#..",
        ".....",
        ".....",
    ]
    assert expand_universe(
        [
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
    ) == [
        "....#........",
        ".........#...",
        "#............",
        ".............",
        ".............",
        "........#....",
        ".#...........",
        "............#",
        ".............",
        ".............",
        ".........#...",
        "#....#.......",
    ]


def main() -> None:
    puzzle = puzzle_file.read_text().splitlines()
    print(play_game(puzzle))


if __name__ == "__main__":
    main()
