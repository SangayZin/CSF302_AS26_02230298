def greedy_earliest_finish(requests):
    """
    Sorts by finish time and picks the request if it doesn't overlap.
    Returns (total_fee, list_of_chosen_indices).
    """
    # Create a list of (finish, start, fee, original_index) so we can sort by finish time
    # while keeping track of the original index in the input list.
    indexed_requests = []
    for i, (start, finish, fee) in enumerate(requests):
        indexed_requests.append((finish, start, fee, i))
    
    # Sort the requests by finish time (the first element in the tuple)
    indexed_requests.sort(key=lambda x: x[0])
    
    total_fee = 0
    chosen_indices = []
    last_finish_time = -1  # Assume time starts at 0 or later
    
    for finish, start, fee, original_index in indexed_requests:
        # If the current request starts after or exactly when the last one finished
        if start >= last_finish_time:
            total_fee += fee
            chosen_indices.append(original_index)
            last_finish_time = finish
            
    # Sort the chosen indices to match the order in the original input
    chosen_indices.sort()
    return (total_fee, chosen_indices)


def greedy_highest_fee(requests):
    """
    Sorts by fee (highest first) and picks the request if it doesn't overlap.
    Returns (total_fee, list_of_chosen_indices).
    """
    # Create a list of (fee, start, finish, original_index)
    indexed_requests = []
    for i, (start, finish, fee) in enumerate(requests):
        indexed_requests.append((fee, start, finish, i))
        
    # Sort by fee descending (highest fee first)
    indexed_requests.sort(key=lambda x: x[0], reverse=True)
    
    total_fee = 0
    chosen_indices = []
    # Keep track of all intervals we have accepted to check for overlaps
    accepted_intervals = []
    
    for fee, start, finish, original_index in indexed_requests:
        # Check if this request overlaps with any already accepted request
        overlap = False
        for acc_start, acc_finish in accepted_intervals:
            # Overlap condition: (Start A < Finish B) AND (Start B < Finish A)
            # Remember: back-to-back is allowed, so we use strict inequality
            if (start < acc_finish) and (acc_start < finish):
                overlap = True
                break
        
        # If it doesn't overlap, accept it
        if not overlap:
            total_fee += fee
            chosen_indices.append(original_index)
            accepted_intervals.append((start, finish))
            
    # Sort the chosen indices to match the order in the original input
    chosen_indices.sort()
    return (total_fee, chosen_indices)

def best_schedule(requests):
    """
    Dynamic Programming solution for Weighted Interval Scheduling.
    Returns (total_fee, list_of_chosen_indices).
    """
    n = len(requests)
    if n == 0:
        return (0, [])

    # Add original indices to keep track of the requests
    indexed_requests = []
    for i, (start, finish, fee) in enumerate(requests):
        indexed_requests.append((start, finish, fee, i))
        
    # Sort the requests by finish time
    indexed_requests.sort(key=lambda x: x[1])

    # p[j] will store the index of the last request that finishes before request j starts.
    # We use 1-based indexing for the DP array, so p[0] is a dummy.
    p = [0] * (n + 1) 
    for j in range(1, n + 1):
        start_j = indexed_requests[j-1][0]
        # Go backwards to find the last compatible request
        for i in range(j - 1, 0, -1):
            finish_i = indexed_requests[i-1][1]
            if finish_i <= start_j:
                p[j] = i
                break

    # OPT[j] stores the maximum fee using a subset of the first j requests
    OPT = [0] * (n + 1)
    
    for j in range(1, n + 1):
        fee_j = indexed_requests[j-1][2]
        # Either we don't include request j (OPT[j-1]), 
        # or we include it and add the best up to p[j] (fee_j + OPT[p[j]])
        OPT[j] = max(OPT[j - 1], fee_j + OPT[p[j]])

    # Reconstruct the chosen requests
    chosen_indices = []
    j = n
    while j > 0:
        fee_j = indexed_requests[j-1][2]
        if fee_j + OPT[p[j]] >= OPT[j - 1]:
            # Request j was included
            original_index = indexed_requests[j-1][3]
            chosen_indices.append(original_index)
            j = p[j]  # Jump to the last compatible request
        else:
            # Request j was not included
            j -= 1

    chosen_indices.sort() # Sort to match the original input order
    return (OPT[n], chosen_indices)


def brute_force(requests):
    """
    Tries every possible subset to find the absolute best schedule.
    Only use for small n (n <= 15).
    Returns (total_fee, list_of_chosen_indices).
    """
    import itertools
    n = len(requests)
    best_fee = 0
    best_subset = []

    # Try every possible length of subset
    for r in range(n + 1):
        # Generate all combinations of size r
        for subset in itertools.combinations(range(n), r):
            current_fee = 0
            valid = True
            
            # Check for overlaps within the subset
            for i in range(len(subset)):
                for k in range(i + 1, len(subset)):
                    idx1 = subset[i]
                    idx2 = subset[k]
                    start1, finish1, _ = requests[idx1]
                    start2, finish2, _ = requests[idx2]
                    
                    # If they overlap, this subset is invalid
                    if (start1 < finish2) and (start2 < finish1):
                        valid = False
                        break
                if not valid:
                    break
            
            # If no overlaps, calculate total fee
            if valid:
                for idx in subset:
                    current_fee += requests[idx][2]
                if current_fee > best_fee:
                    best_fee = current_fee
                    best_subset = list(subset)

    best_subset.sort()
    return (best_fee, best_subset)
