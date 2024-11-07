import dataclasses
import pathlib
from typing import Sequence, TypeAlias


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

ListOfTuples: TypeAlias = list[tuple[int, int, int]]
Seeds = list[int]


@dataclasses.dataclass
class MapInterval:
    start: int
    end: int
    maps_to: int

    def __contains__(self, value: int) -> bool:
        return self.start <= value <= self.end

    def map(self, value: int) -> int:
        return (value - self.start) + self.maps_to


class WeirdDict:
    def __init__(self, ranges: ListOfTuples) -> None:
        self._intervals: list[MapInterval] = []
        for dest_start, source_start, r_lenght in ranges:
            self._intervals.append(
                MapInterval(source_start, source_start + r_lenght - 1, dest_start)
            )
        self._ranges = list(ranges)

    def __str__(self) -> str:
        return f"WeirdDict({self._ranges})"

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, value: int) -> int:
        for interval in self._intervals:
            if value in interval:
                return interval.map(value)
        return value


def parse_range_tuples(text: Sequence[str]) -> ListOfTuples:
    return [
        tuple(map(int, line.split(" "))) for line in text if line
    ]  # pyright: ignore


def parse_puzzle(text: str) -> tuple[Seeds, list[ListOfTuples]]:
    full_seeds_str, *rest = text.split("\n\n")
    _, *seeds_str = full_seeds_str.split(" ")
    seeds = list(map(int, seeds_str))

    result: list[ListOfTuples] = []
    for full_map_str in rest:
        _, *map_str = full_map_str.split("\n")
        result.append(parse_range_tuples(map_str))

    return seeds, result


def play_game(text: str) -> int:
    seeds, map_ranges = parse_puzzle(text)
    print(seeds)
    weird_dicts = [WeirdDict(ranges) for ranges in map_ranges]
    locations: list[int] = []
    for seed in seeds:
        prev_value = seed
        for d in weird_dicts:
            prev_value = d[prev_value]
        locations.append(prev_value)
    return min(locations)


def main() -> None:
    contents = puzzle_file.read_text()
    print(play_game(contents))


def test_weird_map() -> None:
    empty_map = WeirdDict([])
    assert empty_map[10] == 10

    seed2soil = WeirdDict([(50, 98, 2), (52, 50, 48)])
    assert seed2soil[98] == 50
    assert seed2soil[99] == 51

    assert seed2soil[50] == 52
    assert seed2soil[60] == 62

    assert seed2soil[10] == 10
    assert seed2soil[100] == 100


puzzle_1 = """
seeds: 79 14

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

if __name__ == "__main__":
    test_weird_map()
    assert parse_range_tuples(["50 98 2", "52 50 48"]) == [(50, 98, 2), (52, 50, 48)]
    assert parse_puzzle(puzzle_1) == (
        [79, 14],
        [
            [
                (50, 98, 2),
                (52, 50, 48),
            ],
            [
                (0, 15, 37),
                (37, 52, 2),
            ],
        ],
    )
    assert play_game(puzzle_2) == 35
    main()
