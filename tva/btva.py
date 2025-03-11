from tva.voting_schemes import plurality_voting, voting_for_two, anti_plurality_voting, borda_voting
from tva.happiness import compute_happiness
from tva.risk import compute_risk


class BTVA:
    """
    Basic Tactical Voting Analyst that:
    1) Only analyzes single-voter manipulation
    2) Does not consider counter-strategic voting
    3) Has perfect knowledge of voter preferences
    4) Only considers tactical voting by a single voter
    """

    def __init__(self, scheme):
        self.scheme = scheme

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
        Analyze the voting situation and compute:
        - Non-strategic voting outcome
        - Voter happiness levels
        - Strategic voting risk

        Args:
            preferences: List of voter preference lists

        Returns:
            outcome: The non-strategic voting outcome
            happiness_scores: Dictionary of voter happiness scores
            risk: The strategic voting risk
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

        # Calculate strategic voting risk
        risk = compute_risk(preferences, [outcome], self.voting_function)

        return outcome, happiness_scores, risk