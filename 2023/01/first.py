"""
The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""

import pathlib
import re


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"


def extract_first(text: str) -> int:
    return int(next(re.finditer(r"\d", text)).group())


def extract_numbers(text: str) -> int:
    return extract_first(text) * 10 + extract_first(text[::-1])


def main() -> None:
    contents = puzzle_file.read_text().splitlines()
    print(sum(extract_numbers(line) for line in contents))


if __name__ == "__main__":
    assert extract_first("1abc2") == 1
    assert extract_numbers("1abc2") == 12
    assert extract_numbers("pqr3stu8vwx") == 38
    assert extract_numbers("a1b2c3d4e5f") == 15
    assert extract_numbers("treb7uchet") == 77

    main()
