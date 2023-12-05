"""
The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, all with their opaque covering already scratched off. Picking one up, it looks like each card has two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have. You organize the information into a table (your puzzle input).

As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the list of winning numbers. The first match makes the card worth one point and each match after the first doubles the point value of that card.

For example:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86) are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three times for each of the three matches after the first).

    Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
    Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
    Card 4 has one winning number (84), so it is worth 1 point.
    Card 5 has no winning numbers, so it is worth no points.
    Card 6 has no winning numbers, so it is worth no points.

So, in this example, the Elf's pile of scratchcards is worth 13 points.

Take a seat in the large pile of colorful cards. How many points are they worth in total?
"""

import pathlib
import re


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"


def str_to_int_list(text: str) -> list[int]:
    return [int(num_str) for num_str in re.split(r" +", text)]


def get_numbers(text: str) -> tuple[int, list[int], list[int]]:
    card_id, winning_str, having_str = re.split(r": +| +\| +", text)
    id_ = int(re.split(r" +", card_id)[1])
    return id_, str_to_int_list(winning_str), str_to_int_list(having_str)


def calculate_nbr_match(list_1: list[int], list_2: list[int]) -> int:
    return len(set(list_1).intersection(list_2))


def calculate_points(nbr_matches: int) -> int:
    if nbr_matches == 0:
        return 0
    return 2 ** (nbr_matches - 1)


def process_line(text: str) -> int:
    _, winning_list, having_list = get_numbers(text)
    nb_match = calculate_nbr_match(winning_list, having_list)
    return calculate_points(nb_match)


def main() -> None:
    contents: list[str] = puzzle_file.read_text().splitlines()
    print(sum(process_line(content) for content in contents))


if __name__ == "__main__":
    assert str_to_int_list("1 2  3") == [1, 2, 3]
    assert get_numbers("Card  1:  1 48 17 |  3 86  6 31") == (
        1,
        [1, 48, 17],
        [3, 86, 6, 31],
    )
    assert get_numbers("Card 17: 41 48 17 | 83 86  6 31") == (
        17,
        [41, 48, 17],
        [83, 86, 6, 31],
    )
    assert calculate_nbr_match([41, 48, 17], [83, 86, 6, 31]) == 0
    assert calculate_nbr_match([41, 2], [83, 2]) == 1
    assert calculate_nbr_match([41, 2], [83, 2, 41]) == 2
    assert calculate_points(0) == 0
    assert calculate_points(1) == 1
    assert calculate_points(2) == 2
    assert calculate_points(5) == 16
    assert process_line("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53") == 8
    main()
