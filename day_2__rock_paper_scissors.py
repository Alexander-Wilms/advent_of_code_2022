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


def get_RPS_from_strategy_guide(line):
    rps = line.split()
    rps_enum = []
    opponent = map_strategy_guide_opponent_to_enum(rps[0])
    rps_enum.append(opponent)
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


total_score = 0
with open("day_2_input.txt", "r") as f:
    for line in f:
        print(line.strip())
        [opponent, myself] = get_RPS_from_strategy_guide(line.strip())
        pprint(opponent)
        pprint(myself)
        score_of_round = get_score_of_round(opponent, myself)
        print(score_of_round)
        total_score += score_of_round

print(total_score)
