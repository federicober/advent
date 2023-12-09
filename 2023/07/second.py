"""
To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""
import pathlib
import collections
from unittest import mock

import pytest


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

MAP_LETTER_TO_VALUE = {"A": 14, "K": 13, "Q": 12, "T": 10, "J": 0.5}


def hand_encode(cards: str) -> list[int]:
    return [MAP_LETTER_TO_VALUE.get(card) or int(card) for card in cards]


def test_card_encode() -> None:
    assert hand_encode("44423") == [4, 4, 4, 2, 3]
    assert hand_encode("AKQJT") == [14, 13, 12, 1, 10]


def get_main_score(cards: str) -> int:
    encoded = hand_encode(cards)
    counter = collections.Counter(encoded)
    return sum(c**2 for c in counter.values())


def score_hand(cards: str) -> tuple[int, list[int]]:
    main_score = max(get_main_score(cards.replace("J", i)) for i in "23456789TQKA")
    encoded = hand_encode(cards)
    return main_score, encoded


def test_score_hand() -> None:
    assert score_hand("22222") == (25, mock.ANY)
    assert score_hand("33333") == (25, mock.ANY)
    assert score_hand("AAAA2") == (17, mock.ANY)
    assert score_hand("22334") == (9, mock.ANY)
    assert score_hand("2233J") == (13, mock.ANY)
    assert score_hand("2345J") == (7, mock.ANY)
    assert score_hand("23456") == (5, mock.ANY)


def test_compare_score_hand() -> None:
    assert score_hand("3322J") > score_hand("2233J")
    assert score_hand("4444J") > score_hand("44442")
    assert score_hand("44444") > score_hand("4444J")
    assert score_hand("QQQQ2") > score_hand("QJJQ2")
    assert score_hand("QQQQ2") > score_hand("JKKK2")


def parse_puzzle(lines: list[str]) -> list[tuple[str, int]]:
    result = []
    for line in lines:
        hand, bid = line.split(" ")
        result.append((hand, int(bid)))
    return result


@pytest.fixture
def puzzle() -> list[str]:
    return ["32T3K 765", "T55J5 684", "KK677 28", "KTJJT 220", "QQQJA 483"]


def test_parse_puzzle(puzzle: list[str]) -> None:
    assert parse_puzzle(puzzle) == [
        ("32T3K", 765),
        ("T55J5", 684),
        ("KK677", 28),
        ("KTJJT", 220),
        ("QQQJA", 483),
    ]


def play_game(puzzle: list[str]) -> int:
    parsed_hands = parse_puzzle(puzzle)
    ordered = sorted(parsed_hands, key=lambda t: score_hand(t[0]))
    return sum(rank * card[1] for rank, card in enumerate(ordered, start=1))


def test_play_game(puzzle: list[str]) -> None:
    assert play_game(puzzle) == 5905


def main() -> None:
    puzzle = puzzle_file.read_text().splitlines()
    print(play_game(puzzle))


if __name__ == "__main__":
    main()
