"""
You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

"""
import itertools
import pathlib
import re


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"


def parse_puzzle(puzzle: str) -> tuple[str, dict[str, tuple[str, str]]]:
    directions, network = puzzle.split("\n\n")

    directions = directions.strip()
    network = network.strip()
    network_dict: dict[str, tuple[str, str]] = {}

    for line in network.splitlines():
        match = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
        if not match:
            raise ValueError(f"Could not parse line: {line}")
        node, left, right = match.groups()
        network_dict[node] = (left, right)

    return directions, network_dict


def play_game(puzzle: str) -> int:
    directions, network = parse_puzzle(puzzle)

    current_node = "AAA"
    for counter, direction in enumerate(itertools.cycle(directions)):
        left, right = network[current_node]
        if current_node == "ZZZ":
            return counter

        if direction == "L":
            current_node = left
        elif direction == "R":
            current_node = right
        else:
            raise ValueError(f"Invalid direction: {direction}")
    raise RuntimeError("Unreachable")


PUZZLE_1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

PUZZLE_2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


def test_parse_puzzle_1() -> None:
    directions, network = parse_puzzle(PUZZLE_1)

    assert directions == "RL"
    assert network == {
        "AAA": ("BBB", "CCC"),
        "BBB": ("DDD", "EEE"),
        "CCC": ("ZZZ", "GGG"),
        "DDD": ("DDD", "DDD"),
        "EEE": ("EEE", "EEE"),
        "GGG": ("GGG", "GGG"),
        "ZZZ": ("ZZZ", "ZZZ"),
    }


def test_parse_puzzle_2() -> None:
    directions, network = parse_puzzle(PUZZLE_2)

    assert directions == "LLR"
    assert network == {
        "AAA": ("BBB", "BBB"),
        "BBB": ("AAA", "ZZZ"),
        "ZZZ": ("ZZZ", "ZZZ"),
    }


def test_play_game_1() -> None:
    assert play_game(PUZZLE_1) == 2


def test_play_game_2() -> None:
    assert play_game(PUZZLE_2) == 6


def main() -> None:
    puzzle = puzzle_file.read_text()
    print(play_game(puzzle))


if __name__ == "__main__":
    main()
