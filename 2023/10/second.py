"""
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

Your puzzle answer was 6864.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........

The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....

In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........

In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...

The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO

In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?

"""
import itertools
import pathlib
from typing import Iterator

import pytest


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

MAP_CHAR_TO_EXPANDED = {
    ".": [
        "...",
        "...",
        "...",
    ],
    "|": [
        ".|.",
        ".|.",
        ".|.",
    ],
    "-": [
        "...",
        "---",
        "...",
    ],
    "F": [
        "...",
        ".F-",
        ".|.",
    ],
    "L": [
        ".|.",
        ".L-",
        "...",
    ],
    "J": [
        ".|.",
        "-J.",
        "...",
    ],
    "7": [
        "...",
        "-7.",
        ".|.",
    ],
    "S": [
        ".|.",
        "-+-",
        ".|.",
    ],
}


def expand_puzzle(puzzle: list[str]) -> list[str]:
    expanded_puzzle: list[list[str]] = [[] for _ in range(len(puzzle) * 3)]
    for idx, line in enumerate(puzzle):
        for c in line:
            expanded_char = MAP_CHAR_TO_EXPANDED[c]
            for jdx in range(3):
                expanded_puzzle[idx * 3 + jdx].append(expanded_char[jdx])
    return ["".join(line) for line in expanded_puzzle]


def color_puzzle(puzzle: list[str]) -> list[set[tuple[int, int]]]:
    if not puzzle:
        return []
    colored_puzzle: list[list[int]] = [
        [0 for _ in range(len(puzzle[0]))] for _ in range(len(puzzle))
    ]

    def get_next_color_start() -> tuple[int, int] | None:
        for row, (line, color_line) in enumerate(zip(puzzle, colored_puzzle)):
            for col, (char, color) in enumerate(zip(line, color_line)):
                if char == "." and color == 0:
                    return row, col
        return None

    current_color = 0
    result: list[set[tuple[int, int]]] = []
    while next_color_start := get_next_color_start():
        queue = [next_color_start]
        current_color += 1
        result.append(set())

        while queue:
            row, col = queue.pop(0)
            if (
                not (0 <= row < len(colored_puzzle))
                or not (0 <= col < len(colored_puzzle[0]))
                or colored_puzzle[row][col] != 0
                or puzzle[row][col] != "."
            ):
                continue
            colored_puzzle[row][col] = current_color
            result[current_color - 1].add((row, col))
            for new_row, new_col in [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
            ]:
                queue.append((new_row, new_col))
    return result


def drop_boundary_zones(
    zones: list[set[tuple[int, int]]], puzzle: list[str]
) -> list[set[tuple[int, int]]]:
    idx_to_delete: set[int] = set()
    nbr_rows = len(puzzle)
    nbr_cols = len(puzzle[0])
    frontier = set(
        [(idx, 0) for idx in range(nbr_rows)]
        + [(idx, nbr_cols - 1) for idx in range(nbr_rows)]
        + [(0, idx) for idx in range(nbr_cols)]
        + [(nbr_rows - 1, idx) for idx in range(nbr_cols)]
    )
    for coord in frontier:
        for zone_num, zone in enumerate(zones):
            if coord in zone:
                idx_to_delete.add(zone_num)

    return [zones for idx, zones in enumerate(zones) if idx not in idx_to_delete]


def play_game(puzzle: list[str]) -> int:
    only_main_loop = drop_non_main_loop(puzzle)
    # print(*only_main_loop, sep="\n", file=open("no-loop.txt", "w"))
    expanded = expand_puzzle(only_main_loop)
    all_zones = color_puzzle(expanded)
    print("Total of zones:", len(all_zones))
    (center_zones) = drop_boundary_zones(all_zones, expanded)
    print("Total centered zones", len(center_zones))
    expanded_center_zone: list[list[str]] = [["."] * len(line) for line in expanded]

    for row, col in itertools.chain.from_iterable(center_zones):
        if row % 3 == 1 and col % 3 == 1:
            expanded_center_zone[row][col] = "O"
        else:
            expanded_center_zone[row][col] = "x"
    # print(
    #     *("".join(line) for line in expanded_center_zone),
    #     sep="\n",
    #     file=open("out.txt", "w"),
    # )

    return sum(1 for row in expanded_center_zone for char in row if char == "O")


def find_start(puzzle: list[str]) -> tuple[int, int]:
    for row, line in enumerate(puzzle):
        for col, char in enumerate(line):
            if char == "S":
                return row, col
    raise RuntimeError("No start found")


UP_PIPES = ["|", "7", "F"]
RIGHT_PIPES = ["-", "7", "J"]
LEFT_PIPES = ["-", "L", "F"]
DOWN_PIPES = ["|", "J", "L"]
POSSIBLE_PIPES: dict[str, list[tuple[int, int, list[str]]]] = {
    "L": [(-1, 0, UP_PIPES), (0, 1, RIGHT_PIPES)],
    "J": [(-1, 0, UP_PIPES), (0, -1, LEFT_PIPES)],
    "7": [(1, 0, DOWN_PIPES), (0, -1, LEFT_PIPES)],
    "F": [(1, 0, DOWN_PIPES), (0, 1, RIGHT_PIPES)],
    "|": [(1, 0, DOWN_PIPES), (-1, 0, UP_PIPES)],
    "-": [(0, 1, RIGHT_PIPES), (0, -1, LEFT_PIPES)],
    "S": [
        (1, 0, DOWN_PIPES),
        (-1, 0, UP_PIPES),
        (0, 1, RIGHT_PIPES),
        (0, -1, LEFT_PIPES),
    ],
}


def find_neighbours(puzzle: list[str], row: int, col: int) -> Iterator[tuple[int, int]]:
    current_value = puzzle[row][col]
    for row_offset, col_offset, expected_pipes in POSSIBLE_PIPES[current_value]:
        new_row, new_col = row + row_offset, col + col_offset
        if (
            0 <= new_row < len(puzzle)
            and 0 <= new_col < len(puzzle[0])
            and puzzle[new_row][new_col] in expected_pipes
        ):
            yield new_row, new_col


def find_loop(puzzle: list[str]) -> list[list[int]]:
    loop_matrix = [[0 for _ in line] for line in puzzle]
    start = find_start(puzzle)
    queue = [start]
    loop_matrix[start[0]][start[1]] = 1
    visited: set[tuple[int, int]] = {start}
    while queue:
        row, col = queue.pop(0)
        for new_row, new_col in find_neighbours(puzzle, row, col):
            if (new_row, new_col) in visited:
                continue
            visited.add((new_row, new_col))
            loop_matrix[new_row][new_col] = 1
            queue.append((new_row, new_col))
    return loop_matrix


def drop_non_main_loop(puzzle: list[str]) -> list[str]:
    loop_matrix = find_loop(puzzle)
    return [
        "".join(
            char if loop_matrix[row][col] == 1 else "." for col, char in enumerate(line)
        )
        for row, line in enumerate(puzzle)
    ]


def test_drop_non_main_loop() -> None:
    assert drop_non_main_loop(
        [
            "S---7",
            "|F-7|",
            "||.||",
            "|L-J|",
            "L---J",
        ],
    ) == [
        "S---7",
        "|...|",
        "|...|",
        "|...|",
        "L---J",
    ]


def test_game() -> None:
    PUZZLE = [
        "..........",
        ".S------7.",
        ".|F----7|.",
        ".||....||.",
        ".||....||.",
        ".|L-7F-J|.",
        ".|..||..|.",
        ".L--JL--J.",
        "..........",
    ]
    assert play_game(PUZZLE) == 4
    assert (
        play_game(
            [
                ".F----7F7F7F7F-7....",
                ".|F--7||||||||FJ....",
                ".||.FJ||||||||L7....",
                "FJL7L7LJLJ||LJ.L-7..",
                "L--J.L7...LJS7F-7L7.",
                "....F-J..F7FJ|L7L7L7",
                "....L7.F7||L7|.L7L7|",
                ".....|FJLJ|FJ|F7|.LJ",
                "....FJL-7.||.||||...",
                "....L---J.LJ.LJLJ...",
            ]
        )
        == 8
    )
    assert (
        play_game(
            [
                "S---7",
                "|F-7|",
                "||.||",
                "|L-J|",
                "L---J",
            ],
        )
        == 9
    )


@pytest.mark.parametrize(
    "puzzle,expected",
    [
        (
            ["."],
            [
                "...",
                "...",
                "...",
            ],
        ),
        (
            ["."],
            [
                "...",
                "...",
                "...",
            ],
        ),
        (
            ["|"],
            [
                ".|.",
                ".|.",
                ".|.",
            ],
        ),
        (
            ["-"],
            [
                "...",
                "---",
                "...",
            ],
        ),
        (
            ["S"],
            [
                ".|.",
                "-+-",
                ".|.",
            ],
        ),
        (
            ["-|"],
            [
                "....|.",
                "---.|.",
                "....|.",
            ],
        ),
        (
            [
                "F7",
                "LJ",
            ],
            [
                "......",
                ".F--7.",
                ".|..|.",
                ".|..|.",
                ".L--J.",
                "......",
            ],
        ),
    ],
)
def test_expand_puzzle(puzzle: list[str], expected: list[str]) -> None:
    assert expand_puzzle(puzzle) == expected


@pytest.mark.parametrize(
    "puzzle,expected",
    [
        (["."], [{(0, 0)}]),
        ([".."], [{(0, 0), (0, 1)}]),
        (
            [
                "..",
                "..",
            ],
            [{(0, 0), (0, 1), (1, 0), (1, 1)}],
        ),
        (
            [
                ".|.",
                ".|.",
            ],
            [{(0, 0), (1, 0)}, {(0, 2), (1, 2)}],
        ),
        (
            [
                ".|.",
                "---",
                ".|.",
            ],
            [{(0, 0)}, {(0, 2)}, {(2, 0)}, {(2, 2)}],
        ),
        (
            [
                "S-7",
                "|.|",
                "L-J",
            ],
            [{(1, 1)}],
        ),
    ],
)
def test_color_puzzle(puzzle: list[str], expected: list[list[int]]) -> None:
    assert color_puzzle(puzzle) == expected


@pytest.mark.parametrize(
    "puzzle,expected",
    [
        (["."], []),
        ([".."], []),
        (
            [
                "..",
                "..",
            ],
            [],
        ),
        (
            [
                ".|.",
                ".|.",
            ],
            [],
        ),
        (
            [
                ".|.",
                "---",
                ".|.",
            ],
            [],
        ),
        (
            [
                "S-7",
                "|.|",
                "L-J",
            ],
            [{(1, 1)}],
        ),
        (
            [
                "S-|-7",
                "|.|.|",
                "L-|-J",
            ],
            [{(1, 1)}, {(1, 3)}],
        ),
        (
            [
                "S.|-7",
                "|.|.|",
                "L-|-J",
            ],
            [{(1, 3)}],
        ),
    ],
)
def test_color_and_drop_boundary_zones(
    puzzle: list[str], expected: list[list[int]]
) -> None:
    assert drop_boundary_zones(color_puzzle(puzzle), puzzle) == expected


def main() -> None:
    puzzle = puzzle_file.read_text().splitlines()
    print(play_game(puzzle))


if __name__ == "__main__":
    main()
