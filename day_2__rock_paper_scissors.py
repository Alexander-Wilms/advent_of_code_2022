from enum import Enum
from pprint import pprint


class RPS(Enum):
    rock, paper, scissors = range(1, 3+1)


class Outcome(Enum):
    lost = 0
    draw = 3
    won = 6


def get_outcome_of_round(opponent: RPS, myself: RPS) -> Outcome:
    if opponent == myself:
        return Outcome.draw
    elif (opponent == RPS.rock and myself == RPS.scissors) or \
            (opponent == RPS.scissors and myself == RPS.paper) or \
            (opponent == RPS.paper and myself == RPS.rock):
        return Outcome.lost
    else:
        return Outcome(6-get_outcome_of_round(myself, opponent).value)


def get_score_of_round(opponent: RPS, myself: RPS):
    return myself.value + get_outcome_of_round(opponent, myself).value


def get_RPS_from_strategy_guide(line):
    rps = line.split()
    rps_enum = []
    for i in range(2):
        rps_enum.append(map_strategy_guide_to_enum(rps[i]))
    return rps_enum


def map_strategy_guide_to_enum(character) -> RPS:
    match character:
        case 'A' | 'X':
            return RPS.rock
        case 'B' | 'Y':
            return RPS.paper
        case 'C' | 'Z':
            return RPS.scissors


total_score = 0
with open('day_2_input.txt', 'r') as f:
    for line in f:
        print(line.strip())
        [opponent, myself] = get_RPS_from_strategy_guide(line.strip())
        pprint(opponent)
        pprint(myself)
        score_of_round = get_score_of_round(opponent, myself)
        print(score_of_round)
        total_score += score_of_round

print(total_score)
