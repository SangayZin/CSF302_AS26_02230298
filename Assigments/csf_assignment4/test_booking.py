import random
from booking import greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force

def generate_random_requests(max_requests):
    """Generates a random list of requests for testing."""
    n = random.randint(0, max_requests)
    requests = []
    for _ in range(n):
        # Generate random start times and durations
        start = random.randint(1, 50)
        duration = random.randint(1, 10)
        finish = start + duration
        fee = random.randint(100, 1000)
        requests.append((start, finish, fee))
    return requests

def test_dp_vs_brute_force():
    """Checks best_schedule against brute_force on 500 random inputs."""
    for _ in range(500):
        reqs = generate_random_requests(10)
        dp_result = best_schedule(reqs)
        bf_result = brute_force(reqs)
        
        # We only care about the total fee matching, as there can be multiple optimal subsets
        assert dp_result[0] == bf_result[0], f"Failed on {reqs}. DP: {dp_result}, BF: {bf_result}"
    print("[PASS] 500 random tests (DP vs Brute Force)")

def test_edge_cases():
    """Tests specific edge cases."""
    # No requests
    assert best_schedule([]) == (0, [])
    assert greedy_earliest_finish([]) == (0, [])
    
    # One request
    assert best_schedule([(1, 5, 100)]) == (100, [0])
    
    # All overlapping
    overlap_reqs = [(1, 10, 100), (2, 11, 200), (3, 12, 300)]
    assert best_schedule(overlap_reqs) == (300, [2]) # Should pick the highest fee
    
    # None overlapping
    no_overlap_reqs = [(1, 2, 100), (3, 4, 200), (5, 6, 300)]
    assert best_schedule(no_overlap_reqs) == (600, [0, 1, 2])
    
    # Back-to-back (ending at X, starting at X)
    back_to_back = [(1, 5, 100), (5, 10, 200)]
    assert best_schedule(back_to_back) == (300, [0, 1])
    
    print("[PASS] Edge cases")

def test_greedy_equal_fees():
    """Checks that greedy_earliest_finish is optimal when all fees are equal."""
    for _ in range(100):
        reqs = generate_random_requests(15)
        # Set all fees to the same value
        reqs = [(s, f, 500) for (s, f, _) in reqs]
        
        greedy_result = greedy_earliest_finish(reqs)
        optimal_result = best_schedule(reqs)
        
        assert greedy_result[0] == optimal_result[0], f"Failed on {reqs}. Greedy: {greedy_result}, Opt: {optimal_result}"
    print("[PASS] Greedy earliest finish is optimal when fees are equal")

if __name__ == "__main__":
    test_dp_vs_brute_force()
    test_edge_cases()
    test_greedy_equal_fees()
    print("\nAll Part B tests passed successfully!")
