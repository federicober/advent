"""
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

import pathlib
import regex as re
from typing import Iterator

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
MAP_NUMBERS: dict[str, int] = dict(
    zip(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
        range(1, 10),
    )
)


def __extract_all_numbers(text: str) -> Iterator[int]:
    pipe_nums = "|".join(MAP_NUMBERS)
    regex = re.compile(rf"(\d|{pipe_nums})")
    for m in regex.finditer(text, overlapped=True):
        as_str = m.group()
        as_int = int(MAP_NUMBERS.get(as_str, as_str))
        assert 0 < as_int < 10
        yield as_int


def extract_all_numbers(text: str) -> list[int]:
    all_nums = list(__extract_all_numbers(text))
    # print(all_nums)
    return all_nums


def extract_numbers(text: str) -> int:
    if not text:
        return 0
    all_numbers = extract_all_numbers(text)
    two_digit = all_numbers[0] * 10 + all_numbers[-1]
    assert 0 < two_digit < 100
    return two_digit


def main() -> None:
    contents = puzzle_file.read_text().splitlines()
    print(sum(extract_numbers(line) for line in contents))


if __name__ == "__main__":
    assert extract_all_numbers("two1nine") == [2, 1, 9]
    assert extract_numbers("two1nine") == 29
    assert extract_all_numbers("eightwothree") == [8, 2, 3]
    assert extract_numbers("eightwothree") == 83
    assert extract_all_numbers("abcone2threexyz") == [1, 2, 3]
    assert extract_numbers("abcone2threexyz") == 13
    assert extract_all_numbers("xtwone3four") == [2, 1, 3, 4]
    assert extract_numbers("xtwone3four") == 24
    assert extract_numbers("7pqrstsixteen") == 76
    assert extract_numbers("zoneight234") == 14
    assert extract_numbers("4nineeightseven2") == 42

    main()
