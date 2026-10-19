"""
Q3: Binary Search vs Ternary Search (Menu-Driven Program)
Compares the number of comparisons made by both algorithms.
"""

import random

# Global array to be used by the menu
arr = []


# ---------------------------------------------------------------
# 1. BINARY SEARCH (Divides by 2, 1 comparison per step)
# ---------------------------------------------------------------
def binary_search(array, key):
    left, right = 0, len(array) - 1
    comparisons = 0
    
    while left <= right:
        comparisons += 1  # Count the comparison at this step
        mid = (left + right) // 2
        
        if array[mid] == key:
            return mid, comparisons
        elif array[mid] < key:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1, comparisons


# ---------------------------------------------------------------
# 2. TERNARY SEARCH (Divides by 3, requires 2 comparisons per step)
# ---------------------------------------------------------------
def ternary_search(array, key):
    left, right = 0, len(array) - 1
    comparisons = 0
    
    while left <= right:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        
        comparisons += 1
        if array[mid1] == key:
            return mid1, comparisons
            
        comparisons += 1
        if array[mid2] == key:
            return mid2, comparisons
            
        # If not found at mid1 or mid2, figure out which third to search
        if key < array[mid1]:
            right = mid1 - 1
        elif key > array[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1
            
    return -1, comparisons


# ---------------------------------------------------------------
# 3. MENU FUNCTIONS
# ---------------------------------------------------------------
def generate_array():
    global arr
    try:
        n = int(input("Enter number of elements (n): "))
        arr = sorted([random.randint(1, 1000) for _ in range(n)])
        print(f"Generated sorted array of size {n}.")
    except ValueError:
        print("Invalid input. Please enter an integer.")

def display_array():
    if not arr:
        print("Array is empty. Please generate it first.")
    else:
        print("Array:", arr)

def run_search(search_type):
    if not arr:
        print("Array is empty. Please generate it first.")
        return
        
    try:
        key = int(input("Enter key to search: "))
    except ValueError:
        print("Invalid key.")
        return

    if search_type == 'binary':
        idx, comps = binary_search(arr, key)
    else:
        idx, comps = ternary_search(arr, key)
        
    if idx != -1:
        print(f"Key {key} found at index {idx}.")
    else:
        print(f"Key {key} not found.")
    print(f"Comparisons made: {comps}")

def best_case_test():
    """Best case: key is present. We search for the exact middle element."""
    if not arr:
        print("Array is empty.")
        return
        
    # In binary search, the best case is finding the element exactly at the first mid.
    # In ternary, it's finding it at mid1 or mid2.
    print("\n--- BEST CASE TEST (Searching for a key near the middle) ---")
    mid_idx = len(arr) // 2
    key = arr[mid_idx]
    print(f"Searching for key {key} (present in array)...")
    
    _, comps_b = binary_search(arr, key)
    _, comps_t = ternary_search(arr, key)
    
    print(f"Binary Search Comparisons:  {comps_b}")
    print(f"Ternary Search Comparisons: {comps_t}")

def worst_case_test():
    """Worst case: key is absent. This forces the algorithm to exhaust the search."""
    if not arr:
        print("Array is empty.")
        return
        
    print("\n--- WORST CASE TEST (Searching for a key NOT in array) ---")
    key = -999  # Definitely not in our positive array
    print(f"Searching for key {key} (absent)...")
    
    _, comps_b = binary_search(arr, key)
    _, comps_t = ternary_search(arr, key)
    
    print(f"Binary Search Comparisons:  {comps_b}")
    print(f"Ternary Search Comparisons: {comps_t}")

def comparison_table():
    """Runs both searches across increasing n and prints a table."""
    print("\n--- COMPARISON TABLE (Worst case: Key Absent) ---")
    print(f"{'n':>6} | {'Binary Comps':>12} | {'Ternary Comps':>13}")
    print("-" * 38)
    
    global arr # Temporarily save the user's array
    saved_arr = arr.copy()
    
    for n in [10, 50, 100, 500, 1000, 5000, 10000]:
        arr = sorted([random.randint(1, 100000) for _ in range(n)])
        key = -999 # force worst case
        
        _, comps_b = binary_search(arr, key)
        _, comps_t = ternary_search(arr, key)
        
        print(f"{n:>6} | {comps_b:>12} | {comps_t:>13}")
        
    arr = saved_arr # Restore the user's array


# ---------------------------------------------------------------
# 4. MAIN MENU LOOP
# ---------------------------------------------------------------
if __name__ == "__main__":
    while True:
        print("\n" + "=" * 40)
        print("SEARCH ALGORITHM MENU")
        print("=" * 40)
        print("1. Generate n sorted random numbers -> Array")
        print("2. Display Array")
        print("3. Search for a key using Binary Search")
        print("4. Search for a key using Ternary Search")
        print("5. Step/frequency count for best case")
        print("6. Step/frequency count for worst case")
        print("7. Step/frequency count comparison table across n")
        print("8. Exit")
        print("=" * 40)
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            generate_array()
        elif choice == '2':
            display_array()
        elif choice == '3':
            run_search('binary')
        elif choice == '4':
            run_search('ternary')
        elif choice == '5':
            best_case_test()
        elif choice == '6':
            worst_case_test()
        elif choice == '7':
            comparison_table()
        elif choice == '8':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")