import math


def compute_happiness(preferences, outcome):
    """
    Calculate the happiness level for each voter based on the voting outcome.

    Happiness is defined as position-based: the highest preference gets the
    highest happiness value (m), and it decreases by 1 for each position lower.

    Args:
        preferences: List of voter preference lists
        outcome: List of winners (can contain multiple winners in case of tie)

    Returns:
        Dictionary mapping voter index to happiness score
    """
    happiness_scores = {}

    if len(outcome) != 1:
        # In case of a tie, use the lexicographically first winner
        winner = sorted(outcome)[0]
    else:
        winner = outcome[0]

    for i, voter_pref in enumerate(preferences):
        if winner in voter_pref:
            # Position-based happiness: higher = better
            rank = voter_pref.index(winner)
            happiness_scores[i] = len(voter_pref) - rank
        else:
            # If winner not in preferences, assign lowest happiness
            happiness_scores[i] = 0

    return happiness_scores


def compute_sum_happiness(happiness_scores):
    """
    Calculate the sum of all happiness scores.

    Args:
        happiness_scores: Dictionary mapping voter index to happiness score

    Returns:
        Sum of all happiness scores
    """
    valid_scores = [score for score in happiness_scores.values() if not math.isnan(score)]

    if not valid_scores:
        return math.nan

    return sum(valid_scores)