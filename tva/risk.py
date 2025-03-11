import math
import copy
from itertools import combinations


def compute_risk(preferences, outcome, voting_function):
    """
    Compute the risk of strategic voting with a single voter.

    The risk is defined as the minimum number of voters needed to
    change the election outcome, which is always 1 for successful
    single-voter manipulation or math.inf if impossible.

    Args:
        preferences: List of voter preference lists
        outcome: Current voting outcome
        voting_function: Function to use for calculating election results

    Returns:
        risk: 1 if manipulation is possible, math.inf otherwise
    """
    if len(outcome) != 1:
        return math.inf

    original_winner = outcome[0]
    num_voters = len(preferences)

    # Check each voter for possible manipulation
    for voter_idx in range(num_voters):
        # Get all possible alternatives except the original winner
        all_alternatives = set()
        for pref in preferences:
            all_alternatives.update(pref)

        target_alternatives = [alt for alt in all_alternatives if alt != original_winner]

        for target in target_alternatives:
            # Try manipulation to benefit this target
            modified_preferences = copy.deepcopy(preferences)
            voter_pref = modified_preferences[voter_idx]

            # Try different manipulation strategies based on voting scheme
            if voting_function.__name__ == "plurality_voting":
                # Put target first
                if target in voter_pref:
                    voter_pref.remove(target)
                voter_pref.insert(0, target)

            elif voting_function.__name__ == "voting_for_two":
                # Ensure target is in top two positions
                if target in voter_pref:
                    voter_pref.remove(target)
                voter_pref.insert(0, target)

            elif voting_function.__name__ == "anti_plurality_voting":
                # Ensure original winner is last
                if original_winner in voter_pref:
                    voter_pref.remove(original_winner)
                    voter_pref.append(original_winner)

            elif voting_function.__name__ == "borda_voting":
                # Put target first and original winner last
                if target in voter_pref:
                    voter_pref.remove(target)
                if original_winner in voter_pref:
                    voter_pref.remove(original_winner)

                voter_pref.insert(0, target)
                voter_pref.append(original_winner)

            # Test if manipulation was successful
            new_winners = voting_function(modified_preferences)

            if len(new_winners) == 1 and new_winners[0] != original_winner:
                return 1  # Successful manipulation by a single voter
            elif len(new_winners) > 1 and original_winner not in new_winners:
                # Use lexicographical ordering for tie-breaking
                new_winner = sorted(new_winners)[0]
                if new_winner != original_winner:
                    return 1

    return math.inf  # No successful manipulation found