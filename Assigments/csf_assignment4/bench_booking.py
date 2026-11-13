import random
from booking import greedy_earliest_finish, greedy_highest_fee, best_schedule

def generate_random_requests(n, max_time=100, max_fee=1000):
    """Generates n random requests within a given time frame."""
    requests = []
    for _ in range(n):
        start = random.randint(1, max_time)
        # Duration between 1 and 10
        duration = random.randint(1, 10)
        finish = start + duration
        fee = random.randint(100, max_fee)
        requests.append((start, finish, fee))
    return requests

def main():
    num_trials = 1000
    num_requests = 50
    
    # Track totals and worst-case ratios
    sum_ratio_earliest = 0.0
    worst_ratio_earliest = 1.0
    
    sum_ratio_highest = 0.0
    worst_ratio_highest = 1.0
    
    # We want to set a seed so the results are reproducible for the report
    random.seed(42)

    for i in range(num_trials):
        reqs = generate_random_requests(num_requests)
        
        # Get the optimal revenue first
        opt_fee, _ = best_schedule(reqs)
        
        # If the optimal fee is 0 (e.g., no requests generated), skip to avoid division by zero
        if opt_fee == 0:
            continue
            
        # Calculate ratios
        greedy_e_fee, _ = greedy_earliest_finish(reqs)
        greedy_h_fee, _ = greedy_highest_fee(reqs)
        
        ratio_e = greedy_e_fee / opt_fee
        ratio_h = greedy_h_fee / opt_fee
        
        # Update sums
        sum_ratio_earliest += ratio_e
        sum_ratio_highest += ratio_h
        
        # Update worst-case ratios (lowest fraction of optimal)
        if ratio_e < worst_ratio_earliest:
            worst_ratio_earliest = ratio_e
            
        if ratio_h < worst_ratio_highest:
            worst_ratio_highest = ratio_h

    # Calculate averages
    avg_ratio_earliest = sum_ratio_earliest / num_trials
    avg_ratio_highest = sum_ratio_highest / num_trials

    print(f"Results from {num_trials} trials of {num_requests} random requests:")
    print("-" * 60)
    print(f"{'Greedy Rule':<25} | {'Average Ratio':<15} | {'Worst Ratio':<15}")
    print("-" * 60)
    print(f"{'Earliest Finish':<25} | {avg_ratio_earliest:.4f}          | {worst_ratio_earliest:.4f}")
    print(f"{'Highest Fee':<25} | {avg_ratio_highest:.4f}          | {worst_ratio_highest:.4f}")
    print("-" * 60)
    print("\nNote: A ratio of 1.0000 means the greedy rule found the optimal revenue.")
    print("A ratio of 0.8000 means the greedy rule only earned 80% of the optimal revenue.")

if __name__ == "__main__":
    main()
