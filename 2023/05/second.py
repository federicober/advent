"""
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

Your puzzle answer was 346433842.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?

"""
import dataclasses
import itertools
import math
import pathlib
import pytest
from rich.progress import track
from typing import Iterator, Sequence, TypeAlias, overload


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

ListOfTuples: TypeAlias = list[tuple[int, int, int]]
Seeds = Iterator[int]


@dataclasses.dataclass
class Interval:
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError()

    def __contains__(self, value: "int | Interval") -> bool:
        match value:
            case int(_):
                return self.start <= value <= self.end
            case Interval(start, end):
                return self.start <= start and end <= self.end


@dataclasses.dataclass
class MapInterval(Interval):
    dest_range_start: int

    @overload
    def __getitem__(self, value: int) -> int:
        ...

    @overload
    def __getitem__(self, value: Interval) -> Interval:
        ...

    def __getitem__(self, value: int | Interval) -> int | Interval:
        match value:
            case int(_):
                return (value - self.start) + self.dest_range_start
            case Interval(start, end):
                if value in self:
                    return Interval(self[start], self[end])
        raise KeyError(value)


class WeirdDict:
    def __init__(self, ranges: ListOfTuples) -> None:
        self._intervals = [
            MapInterval(source_start, source_start + r_lenght - 1, dest_start)
            for dest_start, source_start, r_lenght in sorted(ranges, key=lambda t: t[1])
        ]

        self._ranges = list(ranges)

    def __str__(self) -> str:
        return f"WeirdDict({self._ranges})"

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, value: Interval) -> list[Interval]:
        for interval in self._intervals:
            try:
                return [interval[value]]
            except KeyError:
                pass
        start, end = value.start, value.end
        result = [value]
        if start < self._intervals[0].start:
            if end < self._intervals[0].start:
                return [value]
            result.append(Interval(start=start, end=self._intervals[0].start - 1))
        return result


def parse_range_tuples(text: Sequence[str]) -> ListOfTuples:
    return [
        tuple(map(int, line.split(" "))) for line in text if line
    ]  # pyright: ignore


def as_intervals(*nums: int) -> list[Interval]:
    return [Interval(start, end) for start, end in itertools.batched(nums, 2)]


def as_intervals_from_len(*nums: int) -> list[Interval]:
    return [
        Interval(start, start + r_len - 1)
        for start, r_len in itertools.batched(nums, 2)
    ]


def parse_puzzle(text: str) -> tuple[list[Interval], list[ListOfTuples]]:
    full_seeds_str, *rest = text.split("\n\n")
    _, *seeds_str = full_seeds_str.split(" ")
    seed_pairs = as_intervals_from_len(*map(int, seeds_str))

    result: list[ListOfTuples] = []
    for full_map_str in rest:
        _, *map_str = full_map_str.split("\n")
        result.append(parse_range_tuples(map_str))

    return seed_pairs, result


def play_game(text: str) -> int:
    seeds, map_ranges = parse_puzzle(text)
    weird_dicts = [WeirdDict(ranges) for ranges in map_ranges]
    min_loc = math.inf

    for seed_iterval in seeds:
        prev_value = seed_iterval
        for d in weird_dicts:
            prev_value = d[prev_value]
        if prev_value < min_loc:
            min_loc = prev_value
    return int(min_loc)


def main() -> None:
    contents = puzzle_file.read_text()
    print(play_game(contents))


@pytest.fixture
def weird_dict() -> WeirdDict:
    # 50 -> 52
    # 51 -> 53
    # ...
    # 96 -> 98
    # 97 -> 99
    # 98 -> 50
    # 99 -> 51
    return WeirdDict([(50, 98, 2), (52, 50, 48)])


def test_weird_map_behaves_with_specs(weird_dict: WeirdDict) -> None:
    assert weird_dict[Interval(98, 98)] == as_intervals(50, 50)
    assert weird_dict[Interval(99, 99)] == as_intervals(51, 51)
    assert weird_dict[Interval(50, 50)] == as_intervals(52, 52)
    assert weird_dict[Interval(60, 60)] == as_intervals(62, 62)


def test_weird_dict_does_easy_intervals(weird_dict: WeirdDict) -> None:
    assert weird_dict[Interval(50, 60)] == as_intervals(52, 62)


def test_weird_dict_does_respects_non_mapped_values(weird_dict: WeirdDict) -> None:
    assert weird_dict[Interval(10, 10)] == [Interval(10, 10)]


def test_weird_dict_does_difficult_intervals(weird_dict: WeirdDict) -> None:
    assert weird_dict[Interval(45, 51)] == as_intervals(45, 49, 52, 53)
    assert weird_dict[Interval(96, 99)] == as_intervals(98, 99, 50, 51)

    assert weird_dict[Interval(100, 100)] == [Interval(100, 100)]


def test_empty_weird_dir_acts_as_identity() -> None:
    empty_map = WeirdDict([])
    assert empty_map[Interval(10, 10)] == [Interval(10, 10)]


puzzle_1 = """
seeds: 79 2 100 3

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
""".strip()

puzzle_2 = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".strip()


def test_parse_puzzle() -> None:
    seeds, tuples = parse_puzzle(puzzle_1)
    assert list(seeds) == [Interval(79, 80), Interval(100, 102)]
    assert tuples == [
        [
            (50, 98, 2),
            (52, 50, 48),
        ],
        [
            (0, 15, 37),
            (37, 52, 2),
        ],
    ]


def test_play_game() -> None:
    assert play_game(puzzle_2) == 46


def test_parse_range_tuples() -> None:
    assert parse_range_tuples(["50 98 2", "52 50 48"]) == [(50, 98, 2), (52, 50, 48)]


if __name__ == "__main__":
    main()
