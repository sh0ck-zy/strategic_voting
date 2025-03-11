import math
import random
import time
from tva.btva import BTVA
from tva.atva1 import ATVA1
from tva.happiness import compute_sum_happiness
from tva.generate_situation import generate_preferences


def run_simulation(voting_scheme, num_voters, num_candidates, num_simulations):
    """
    Runs num_simulations simulations for a given voting scheme, number of voters, and number of candidates.
    Returns statistics: average risk, average happiness, and percentage of successful manipulations.
    """
    btva_results = []
    atva1_results = []

    # Set timeout for simulations
    timeout_per_simulation = 180  # 3 minutes per simulation
    start_time_total = time.time()

    for i in range(num_simulations):
        print(
            f"Running simulation {i + 1}/{num_simulations} for {voting_scheme}, {num_voters} voters, {num_candidates} candidates")
        start_time_sim = time.time()

        # Generate random preferences
        preferences = generate_preferences(num_candidates, num_voters)

        # BTVA analysis (individual manipulation)
        btva = BTVA(scheme=voting_scheme)
        outcome_btva, happiness_scores_btva, risk_btva = btva.analyse(preferences)
        sum_happiness_btva = compute_sum_happiness(happiness_scores_btva)

        # Time check before ATVA-1
        elapsed_time = time.time() - start_time_sim
        if elapsed_time > timeout_per_simulation / 2:
            print(f"Warning: BTVA analysis took too long ({elapsed_time:.2f}s), skipping ATVA-1")
            risk_atva1 = math.inf
            sum_happiness_atva1 = sum_happiness_btva
        else:
            # ATVA-1 analysis (group collusion)
            try:
                atva1 = ATVA1(scheme=voting_scheme, debug=False)
                outcome_atva1, happiness_scores_atva1, risk_atva1 = atva1.analyse(preferences)
                sum_happiness_atva1 = compute_sum_happiness(happiness_scores_atva1)
            except Exception as e:
                print(f"Error in ATVA-1 analysis: {e}")
                risk_atva1 = math.inf
                sum_happiness_atva1 = sum_happiness_btva

        btva_results.append((risk_btva, sum_happiness_btva))
        atva1_results.append((risk_atva1, sum_happiness_atva1))

        # Check if we've hit the timeout for all simulations
        if time.time() - start_time_total > timeout_per_simulation * num_simulations:
            print(f"Warning: Total simulation time exceeded. Stopping after {i + 1} simulations")
            break

        print(f"Simulation {i + 1} completed in {time.time() - start_time_sim:.2f}s")

    # Calculate averages
    if btva_results:
        avg_risk_btva = sum([r if r != math.inf else 0 for r, _ in btva_results]) / len(btva_results)
        avg_happiness_btva = sum([h for _, h in btva_results]) / len(btva_results)
        success_btva = sum([1 for r, _ in btva_results if r != math.inf]) / len(btva_results) * 100

        avg_risk_atva1 = sum([r if r != math.inf else 0 for r, _ in atva1_results]) / len(atva1_results)
        avg_happiness_atva1 = sum([h for _, h in atva1_results]) / len(atva1_results)
        success_atva1 = sum([1 for r, _ in atva1_results if r != math.inf]) / len(atva1_results) * 100
    else:
        avg_risk_btva = avg_risk_atva1 = avg_happiness_btva = avg_happiness_atva1 = success_btva = success_atva1 = 0

    return {
        "avg_risk_btva": avg_risk_btva,
        "avg_risk_atva1": avg_risk_atva1,
        "avg_happiness_btva": avg_happiness_btva,
        "avg_happiness_atva1": avg_happiness_atva1,
        "success_btva": success_btva,
        "success_atva1": success_atva1,
        "completed_simulations": len(btva_results)
    }


def simulation_experiments():
    """
    Runs simulation experiments for various voting schemes,
    numbers of voters, and numbers of candidates.
    """
    voting_schemes = ["plurality", "voting_for_two", "anti_plurality", "borda"]
    num_simulations = 10  # Number of simulations for each scenario
    voters_list = [25, 50, 100]
    candidates_list = [5, 10]

    for scheme in voting_schemes:
        print("===========================================")
        print(f"Voting Scheme: {scheme.upper()}")
        for num_voters in voters_list:
            for num_candidates in candidates_list:
                print(f"Starting analysis for {num_voters} voters and {num_candidates} candidates")
                start_time = time.time()

                results = run_simulation(scheme, num_voters, num_candidates, num_simulations)

                print(f"Voters: {num_voters}, Candidates: {num_candidates}")
                print(f"  Completed {results['completed_simulations']} of {num_simulations} simulations")
                print(
                    f"  BTVA: Avg Risk: {results['avg_risk_btva']:.2f}, Avg Happiness: {results['avg_happiness_btva']:.2f}, "
                    f"Successful Manipulation: {results['success_btva']:.1f}%")
                print(
                    f"  ATVA-1: Avg Risk: {results['avg_risk_atva1']:.2f}, Avg Happiness: {results['avg_happiness_atva1']:.2f}, "
                    f"Successful Manipulation: {results['success_atva1']:.1f}%")
                print(f"  Time taken: {time.time() - start_time:.2f}s")
                print("-------------------------------------------")
        print("===========================================")


def custom_scenario():
    """
    Demonstrates a custom (manually defined) scenario and displays the results from
    both the BTVA and ATVA-1 analyses for each voting scheme.
    """
    preferences = [
        # 10 voters preferring P1
        ['P1', 'P2', 'P3', 'P4', 'P5'],
        ['P1', 'P2', 'P3', 'P4', 'P5'],
        ['P1', 'P2', 'P3', 'P4', 'P5'],
        ['P1', 'P2', 'P3', 'P4', 'P5'],
        ['P1', 'P3', 'P2', 'P4', 'P5'],
        ['P1', 'P3', 'P2', 'P4', 'P5'],
        ['P1', 'P3', 'P2', 'P4', 'P5'],
        ['P1', 'P4', 'P2', 'P3', 'P5'],
        ['P1', 'P4', 'P2', 'P3', 'P5'],
        ['P1', 'P4', 'P3', 'P2', 'P5'],
        # 7 voters preferring P2
        ['P2', 'P3', 'P1', 'P4', 'P5'],
        ['P2', 'P3', 'P1', 'P4', 'P5'],
        ['P2', 'P3', 'P1', 'P4', 'P5'],
        ['P2', 'P1', 'P3', 'P4', 'P5'],
        ['P2', 'P1', 'P3', 'P4', 'P5'],
        ['P2', 'P4', 'P1', 'P3', 'P5'],
        ['P2', 'P4', 'P3', 'P1', 'P5'],
        # 4 voters preferring P3
        ['P3', 'P2', 'P1', 'P4', 'P5'],
        ['P3', 'P2', 'P1', 'P4', 'P5'],
        ['P3', 'P2', 'P4', 'P1', 'P5'],
        ['P3', 'P4', 'P2', 'P1', 'P5'],
        # 4 voters preferring P4
        ['P4', 'P3', 'P2', 'P1', 'P5'],
        ['P4', 'P3', 'P2', 'P1', 'P5'],
        ['P4', 'P2', 'P3', 'P1', 'P5'],
        ['P4', 'P1', 'P2', 'P3', 'P5']
    ]
    print("===== Custom Voter Preferences =====")
    for i, prefs in enumerate(preferences):
        print(f"Voter {i + 1}: {prefs}")
    print()

    voting_schemes = ["plurality", "voting_for_two", "anti_plurality", "borda"]
    for scheme in voting_schemes:
        print("===========================================")
        print(f"Voting Scheme: {scheme.upper()}")

        try:
            # BTVA Analysis
            btva = BTVA(scheme=scheme)
            outcome_btva, happiness_scores_btva, risk_btva = btva.analyse(preferences)
            sum_happiness_btva = compute_sum_happiness(happiness_scores_btva)
            print("-> BTVA Results:")
            print(
                f"   Outcome: {outcome_btva}, Sum of Happiness: {sum_happiness_btva}, Risk: {risk_btva if risk_btva != math.inf else 'No manipulation possible'}")

            # ATVA-1 Analysis
            atva1 = ATVA1(scheme=scheme, debug=True)
            outcome_atva1, happiness_scores_atva1, risk_atva1 = atva1.analyse(preferences)
            sum_happiness_atva1 = compute_sum_happiness(happiness_scores_atva1)
            print("-> ATVA-1 Results:")
            print(
                f"   Outcome: {outcome_atva1}, Sum of Happiness: {sum_happiness_atva1}, Risk: {risk_atva1 if risk_atva1 != math.inf else 'No manipulation possible'}")
        except Exception as e:
            print(f"Error analyzing with {scheme}: {e}")

        print("===========================================")
        print()


def main():
    print("Choose mode:")
    print("  1 - Custom Scenario")
    print("  2 - Simulation Experiments")
    mode = input("Option: ")
    if mode == "1":
        custom_scenario()
    elif mode == "2":
        simulation_experiments()
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()