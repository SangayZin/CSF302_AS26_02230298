from booking import greedy_earliest_finish, greedy_highest_fee, best_schedule

def test_counterexamples():
    print("--- Counterexample 1: Greedy Earliest Finish fails ---")
    # Request 0 is short but low fee. It blocks Request 1 which is long but high fee.
    # Greedy will pick 0, then 2. DP will pick 1.
    reqs1 = [
        (1, 3, 50),    # 0: starts 1, ends 3, fee 50
        (2, 10, 500),  # 1: starts 2, ends 10, fee 500
        (4, 11, 400)   # 2: starts 4, ends 11, fee 400
    ]
    
    g_earliest = greedy_earliest_finish(reqs1)
    optimal1 = best_schedule(reqs1)
    
    print(f"Greedy Earliest Finish: fee={g_earliest[0]}, chosen={g_earliest[1]}")
    print(f"Optimal (DP):           fee={optimal1[0]}, chosen={optimal1[1]}")
    assert g_earliest[0] < optimal1[0], "Greedy Earliest Finish did not fail as expected!"
    print("[PASS] Earliest Finish earns less than optimal.\n")

    print("--- Counterexample 2: Greedy Highest Fee fails ---")
    # Request 0 has the highest fee, but blocks requests 1 and 2 which together pay more.
    # Greedy will pick 0. DP will pick 1 and 2.
    reqs2 = [
        (1, 10, 1000), # 0: highest fee, spans the whole time
        (1, 5, 600),   # 1: fits in the first half
        (6, 10, 600)   # 2: fits in the second half
    ]
    
    g_highest = greedy_highest_fee(reqs2)
    optimal2 = best_schedule(reqs2)
    
    print(f"Greedy Highest Fee:     fee={g_highest[0]}, chosen={g_highest[1]}")
    print(f"Optimal (DP):           fee={optimal2[0]}, chosen={optimal2[1]}")
    assert g_highest[0] < optimal2[0], "Greedy Highest Fee did not fail as expected!"
    print("[PASS] Highest Fee earns less than optimal.\n")

if __name__ == "__main__":
    test_counterexamples()
