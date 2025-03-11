def plurality_voting(preferences):
    """
    Plurality voting scheme: each voter gives one vote to their top preference.
    Voting vector: [1, 0, 0, ...]

    Returns a list of winners (can be multiple in case of a tie)
    """
    vote_counts = {}

    for voter_pref in preferences:
        if not voter_pref:  # Skip empty preference lists
            continue
        first_choice = voter_pref[0]
        vote_counts[first_choice] = vote_counts.get(first_choice, 0) + 1

    if not vote_counts:  # Handle case with no valid votes
        return []

    max_votes = max(vote_counts.values())
    winners = [candidate for candidate, votes in vote_counts.items() if votes == max_votes]

    return winners


def voting_for_two(preferences):
    """
    Voting for two scheme: each voter gives one vote to their top two preferences.
    Voting vector: [1, 1, 0, 0, ...]

    Returns a list of winners (can be multiple in case of a tie)
    """
    vote_counts = {}

    for voter_pref in preferences:
        # Process up to the first two preferences
        for i in range(min(2, len(voter_pref))):
            choice = voter_pref[i]
            vote_counts[choice] = vote_counts.get(choice, 0) + 1

    if not vote_counts:  # Handle case with no valid votes
        return []

    max_votes = max(vote_counts.values())
    winners = [candidate for candidate, votes in vote_counts.items() if votes == max_votes]

    return winners


def anti_plurality_voting(preferences):
    """
    Anti-plurality (veto) voting scheme: each voter gives one vote to all but their last preference.
    Voting vector: [1, 1, ..., 1, 0]

    Returns a list of winners (can be multiple in case of a tie)
    """
    # First identify all possible candidates
    all_candidates = set()
    for pref in preferences:
        all_candidates.update(pref)

    vote_counts = {candidate: 0 for candidate in all_candidates}

    for voter_pref in preferences:
        if not voter_pref:  # Skip empty preference lists
            continue

        # Give one vote to every candidate except the last preference
        for candidate in all_candidates:
            # If candidate is not in preferences or not the last preference, give a vote
            if candidate not in voter_pref or candidate != voter_pref[-1]:
                vote_counts[candidate] = vote_counts.get(candidate, 0) + 1

    if not vote_counts:  # Handle case with no valid votes
        return []

    max_votes = max(vote_counts.values())
    winners = [candidate for candidate, votes in vote_counts.items() if votes == max_votes]

    return winners


def borda_voting(preferences):
    """
    Borda voting scheme: each candidate gets points based on their rank.
    For m alternatives, the voting vector is [m-1, m-2, ..., 1, 0]

    Returns a list of winners (can be multiple in case of a tie)
    """
    # First identify all possible candidates and the maximum length of preferences
    all_candidates = set()
    max_length = 0

    for pref in preferences:
        all_candidates.update(pref)
        max_length = max(max_length, len(pref))

    vote_counts = {candidate: 0 for candidate in all_candidates}

    for voter_pref in preferences:
        if not voter_pref:  # Skip empty preference lists
            continue

        # Assign Borda points based on position
        for position, candidate in enumerate(voter_pref):
            # Points = m-1-position
            points = max_length - 1 - position
            vote_counts[candidate] = vote_counts.get(candidate, 0) + points

    if not vote_counts:  # Handle case with no valid votes
        return []

    max_votes = max(vote_counts.values())
    winners = [candidate for candidate, votes in vote_counts.items() if votes == max_votes]

    return winners