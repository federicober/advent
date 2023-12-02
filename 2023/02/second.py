"""
As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
    Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
    Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
    Game 4 required at least 14 red, 3 green, and 15 blue cubes.
    Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
"""

import functools
import operator
import pathlib


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"


def element_wise_max(dict1: dict[str, int], dict2: dict[str, int]) -> dict[str, int]:
    return {k: max(dict1.get(k, 0), dict2.get(k, 0)) for k in dict1 | dict2}


def clean_pair(text: str) -> tuple[str, int]:
    num, color = text.split(" ")
    return color, int(num)


def clean_handul(text: str) -> dict[str, int]:
    return dict(clean_pair(pair) for pair in text.split(", "))


def clean_game(text: str) -> list[dict[str, int]]:
    _, without_id = text.split(": ", maxsplit=1)
    return [clean_handul(hand) for hand in without_id.split("; ")]


def __get_minum_set(game: list[dict[str, int]]) -> dict[str, int]:
    return functools.reduce(element_wise_max, game)


def get_minum_set(text: str) -> dict[str, int]:
    game = clean_game(text)
    return __get_minum_set(game)


def get_power(text: str) -> int:
    min_set = get_minum_set(text)
    return functools.reduce(operator.mul, min_set.values())


def main() -> None:
    contents = puzzle_file.read_text().splitlines()
    print(sum(get_power(line) for line in contents))


if __name__ == "__main__":
    assert clean_pair("1 blue") == ("blue", 1)
    assert clean_handul("1 blue, 2 green") == {"blue": 1, "green": 2}
    assert clean_game(
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    )[:2] == [dict(blue=1, green=2), dict(green=3, blue=4, red=1)]
    assert element_wise_max(dict(blue=1), dict(blue=2)) == dict(blue=2)
    assert element_wise_max(dict(blue=1, green=3), dict(blue=2)) == dict(
        blue=2, green=3
    )
    assert element_wise_max(dict(blue=1, green=3), dict(blue=2, green=1)) == dict(
        blue=2, green=3
    )
    assert get_minum_set(
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    ) == dict(blue=6, red=4, green=2)
    assert get_power("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == 48

    main()
