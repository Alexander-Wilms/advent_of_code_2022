import os
from enum import Enum
from pprint import pprint


class RPS(Enum):
    rock, paper, scissors = range(1, 3 + 1)


class Outcome(Enum):
    lost = 0
    draw = 3
    won = 6


def get_outcome_of_round(opponent: RPS, myself: RPS) -> Outcome:
    if opponent == myself:
        return Outcome.draw
    elif (
        (opponent == RPS.rock and myself == RPS.scissors)
        or (opponent == RPS.scissors and myself == RPS.paper)
        or (opponent == RPS.paper and myself == RPS.rock)
    ):
        return Outcome.lost
    else:
        inverted_outcome = get_outcome_of_round(myself, opponent)
        pprint(inverted_outcome)
        print(6 - inverted_outcome.value)
        return Outcome(6 - inverted_outcome.value)


def get_score_of_round(opponent: RPS, myself: RPS):
    pprint(opponent)
    pprint(myself)
    return myself.value + get_outcome_of_round(opponent, myself).value


def get_RPS_from_strategy_guide(line, puzzle_part) -> list[RPS]:
    rps = line.split()
    rps_enum = []
    opponent = map_strategy_guide_opponent_to_enum(rps[0])
    rps_enum.append(opponent)
    if puzzle_part == 1:
        myself = map_strategy_guide_myself_to_enum(rps[1])
        rps_enum.append(myself)
    elif puzzle_part == 2:
        myself = map_strategy_guide_myself_to_Outcome_enum(rps[1])
        rps_enum.append(map_strategy_guide_myself_to_RPS_enum(opponent, myself))
    return rps_enum


def map_strategy_guide_opponent_to_enum(character) -> RPS:
    match character:
        case "A":
            return RPS.rock
        case "B":
            return RPS.paper
        case "C":
            return RPS.scissors


def map_strategy_guide_myself_to_enum(character) -> RPS:
    match character:
        case "X":
            return RPS.rock
        case "Y":
            return RPS.paper
        case "Z":
            return RPS.scissors


def map_strategy_guide_myself_to_Outcome_enum(myself: str) -> Outcome:
    match myself:
        case "X":
            return Outcome.lost
        case "Y":
            return Outcome.draw
        case "Z":
            return Outcome.won


def map_strategy_guide_myself_to_RPS_enum(opponent: RPS, myself: Outcome) -> RPS:
    match myself:
        case Outcome.draw:
            return opponent
        case Outcome.lost:
            return get_myself_lost(opponent)
        case Outcome.won:
            return get_myself_won(opponent)
        case _:
            raise ValueError("Could not match " + str(opponent) + " and " + str(myself))


def get_myself_lost(opponent: RPS) -> RPS:
    match opponent:
        case RPS.rock:
            return RPS.scissors
        case RPS.paper:
            return RPS.rock
        case RPS.scissors:
            return RPS.paper


def get_myself_won(opponent: RPS) -> RPS:
    match opponent:
        case RPS.rock:
            return RPS.paper
        case RPS.paper:
            return RPS.scissors
        case RPS.scissors:
            return RPS.rock


def get_solutions(input_file) -> tuple[int]:
    total_score_part_1 = 0
    total_score_part_2 = 0
    with open(os.path.join(os.path.dirname(__file__), input_file)) as file:
        for line in file:
            print(line.strip())
            [opponent, myself_1] = get_RPS_from_strategy_guide(line.strip(), 1)
            [_, myself_2] = get_RPS_from_strategy_guide(line.strip(), 2)
            pprint(opponent)
            # pprint(myself)
            score_of_round_1 = get_score_of_round(opponent, myself_1)
            score_of_round_2 = get_score_of_round(opponent, myself_2)
            print(score_of_round_1)
            print(score_of_round_2)
            total_score_part_1 += score_of_round_1
            total_score_part_2 += score_of_round_2

    print(f"solution to part 1: {total_score_part_1}")
    print(f"solution to part 2: {total_score_part_2}")

    return total_score_part_1, total_score_part_2


get_solutions("input.txt")
