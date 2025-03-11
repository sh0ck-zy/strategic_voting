from tva.voting_schemes import plurality_voting, voting_for_two, anti_plurality_voting, borda_voting
from tva.happiness import compute_happiness, compute_sum_happiness
import copy
import math
import random
from itertools import combinations


class ATVA1:
    """
    Advanced Tactical Voting Analyst that removes limitation #1:
    Considers multiple-voter manipulation (voter collusion)
    """

    def __init__(self, scheme, debug=False):
        self.scheme = scheme
        self.debug = debug

        # Map scheme names to voting functions
        self.voting_functions = {
            "plurality": plurality_voting,
            "voting_for_two": voting_for_two,
            "anti_plurality": anti_plurality_voting,
            "borda": borda_voting
        }

        if scheme not in self.voting_functions:
            raise ValueError(f"Unsupported voting scheme: {scheme}")

        self.voting_function = self.voting_functions[scheme]

    def analyse(self, preferences):
        """
        Analyze the voting situation considering voter collusion

        Args:
            preferences: List of voter preference lists

        Returns:
            outcome: The non-strategic voting outcome
            happiness_scores: Dictionary of voter happiness scores
            risk: The strategic voting risk considering voter collusion
        """
        # Calculate the non-strategic outcome
        winners = self.voting_function(preferences)

        if len(winners) == 1:
            outcome = winners[0]
        else:
            # In case of a tie, use lexicographical order as specified in the assignment
            outcome = sorted(winners)[0]
            winners = [outcome]  # Update winners to contain only the tie-breaking winner

        # Calculate voter happiness for the non-strategic outcome
        happiness_scores = compute_happiness(preferences, [outcome])

        # Calculate strategic voting risk with voter collusion
        risk = self.compute_collusion_risk(preferences, [outcome])

        if self.debug:
            print(f"Non-strategic outcome: {outcome}")
            print(f"Happiness scores: {happiness_scores}")
            print(f"Sum happiness: {compute_sum_happiness(happiness_scores)}")
            print(f"Strategic voting risk: {risk}")

        return outcome, happiness_scores, risk

    def compute_collusion_risk(self, preferences, outcome):
        """Optimized version that limits computation time"""
        if len(outcome) != 1:
            return math.inf

        original_winner = outcome[0]
        num_voters = len(preferences)

        # Set a stricter upper limit for group size based on number of voters
        if num_voters <= 25:
            max_group_size = min(5, num_voters)
        elif num_voters <= 50:
            max_group_size = min(4, num_voters)
        else:
            max_group_size = min(3, num_voters)

        for k in range(1, max_group_size + 1):
            # For large voter pools, limit the number of combinations to check
            max_combinations_to_check = 1000

            if self.debug:
                print(f"Testing groups of {k} voters")

            # Generate all possible combinations of k voters
            all_combinations = list(combinations(range(num_voters), k))

            # If there are too many combinations, randomly sample a subset
            if len(all_combinations) > max_combinations_to_check:
                random.shuffle(all_combinations)
                combinations_to_check = all_combinations[:max_combinations_to_check]
            else:
                combinations_to_check = all_combinations

            if self.debug:
                print(f"Checking {len(combinations_to_check)} out of {len(all_combinations)} possible combinations")

            # Check each combination
            for voters_group in combinations_to_check:
                if self.can_change_outcome(preferences, voters_group, original_winner):
                    if self.debug:
                        print(f"Found successful manipulation with {k} voters: {voters_group}")
                    return k

            if self.debug:
                print(f"No successful manipulation found with {k} voters")

        return math.inf

    def can_change_outcome(self, preferences, voters_group, original_winner):
        """
        Check if a group of voters can change the election outcome through
        tactical voting.

        Args:
            preferences: List of voter preference lists
            voters_group: Tuple of voter indices who are collaborating
            original_winner: The current winner to be defeated

        Returns:
            bool: True if the group can change the outcome, False otherwise
        """
        # Get the unique alternatives from all preferences
        all_alternatives = set()
        for pref in preferences:
            all_alternatives.update(pref)

        # Remove the current winner from potential targets
        target_alternatives = [alt for alt in all_alternatives if alt != original_winner]

        if not target_alternatives:
            return False

        # For each possible target alternative, check if the group can make it win
        for target in target_alternatives:
            # Try different collusion strategies for this target
            modified_preferences = copy.deepcopy(preferences)

            # For each voter in the collusion group, modify their preference
            for voter_idx in voters_group:
                if self.scheme == "plurality":
                    # For plurality, put the target at the first position
                    if target in modified_preferences[voter_idx]:
                        modified_preferences[voter_idx].remove(target)
                    modified_preferences[voter_idx].insert(0, target)

                elif self.scheme == "voting_for_two":
                    # For voting for two, ensure target is in first position
                    if target in modified_preferences[voter_idx]:
                        modified_preferences[voter_idx].remove(target)
                    modified_preferences[voter_idx].insert(0, target)

                elif self.scheme == "anti_plurality":
                    # For anti_plurality, ensure original winner is last
                    if original_winner in modified_preferences[voter_idx]:
                        modified_preferences[voter_idx].remove(original_winner)
                        modified_preferences[voter_idx].append(original_winner)

                elif self.scheme == "borda":
                    # For Borda, put target first and original_winner last
                    if target in modified_preferences[voter_idx]:
                        modified_preferences[voter_idx].remove(target)
                    if original_winner in modified_preferences[voter_idx]:
                        modified_preferences[voter_idx].remove(original_winner)

                    modified_preferences[voter_idx].insert(0, target)
                    modified_preferences[voter_idx].append(original_winner)

            # Check if the manipulation worked
            new_winners = self.voting_function(modified_preferences)

            if len(new_winners) == 1 and new_winners[0] != original_winner:
                return True
            elif len(new_winners) > 1:
                # Check if original winner is not among the winners or is not the lexicographic first
                if original_winner not in new_winners:
                    return True
                elif sorted(new_winners)[0] != original_winner:
                    return True

        return False