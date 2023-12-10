"""
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
"""
import pathlib
from typing import Iterator


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"


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


def find_neightbours(
    puzzle: list[str], row: int, col: int
) -> Iterator[tuple[int, int]]:
    current_value = puzzle[row][col]
    for row_offset, col_offset, expected_pipes in POSSIBLE_PIPES[current_value]:
        new_row, new_col = row + row_offset, col + col_offset
        if (
            0 <= new_row < len(puzzle)
            and 0 <= new_col < len(puzzle[0])
            and puzzle[new_row][new_col] in expected_pipes
        ):
            yield new_row, new_col


def play_game(puzzle: list[str]) -> int:
    distance_matrix = [[0 for _ in line] for line in puzzle]
    start = find_start(puzzle)
    queue = [start]
    visited: set[tuple[int, int]] = {start}
    while queue:
        row, col = queue.pop(0)
        for new_row, new_col in find_neightbours(puzzle, row, col):
            if (new_row, new_col) in visited:
                continue
            visited.add((new_row, new_col))
            # print((row, col), new_row, new_col)
            distance_matrix[new_row][new_col] = distance_matrix[row][col] + 1
            queue.append((new_row, new_col))
    # print(*distance_matrix, sep="\n")
    return max(map(max, distance_matrix))


PUZZLE_1 = [
    ".....",
    ".S-7.",
    ".|.|.",
    ".L-J.",
    ".....",
]


PUZZLE_2 = [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ...",
]


def test_find_start() -> None:
    assert find_start(PUZZLE_1) == (1, 1)
    assert find_start(PUZZLE_2) == (2, 0)


def test_play_game() -> None:
    assert play_game(PUZZLE_1) == 4

    assert play_game(PUZZLE_2) == 8


def main() -> None:
    puzzle = puzzle_file.read_text().splitlines()
    print(play_game(puzzle))


if __name__ == "__main__":
    main()
