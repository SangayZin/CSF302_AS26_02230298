"""
Lab 3 - Q2: Karatsuba's Algorithm for Large Integer Multiplication
Compares Traditional O(n^2) vs Karatsuba O(n^1.585) algorithm.
Numbers are handled as strings to support up to 1024 digits.
"""

import random
import time


# ---------------------------------------------------------------
# 1. HELPER FUNCTIONS (String Math)
#    Since numbers are huge, we do addition and subtraction
#    character by character (like we do on paper).
# ---------------------------------------------------------------
def string_add(num1, num2):
    """Adds two numbers represented as strings."""
    # Ensure num1 is the longer string
    if len(num1) < len(num2):
        num1, num2 = num2, num1
        
    num1, num2 = num1[::-1], num2[::-1] # Reverse for easy calculation
    carry = 0
    result = []
    
    for i in range(len(num1)):
        d1 = int(num1[i])
        d2 = int(num2[i]) if i < len(num2) else 0
        
        total = d1 + d2 + carry
        result.append(str(total % 10))
        carry = total // 10
        
    if carry:
        result.append(str(carry))
        
    return ''.join(result[::-1]).lstrip('0') or '0'


def string_sub(num1, num2):
    """Subtracts num2 from num1 (assumes num1 >= num2)."""
    num1, num2 = num1[::-1], num2[::-1]
    borrow = 0
    result = []
    
    for i in range(len(num1)):
        d1 = int(num1[i])
        d2 = int(num2[i]) if i < len(num2) else 0
        
        diff = d1 - d2 - borrow
        if diff < 0:
            diff += 10
            borrow = 1
        else:
            borrow = 0
        result.append(str(diff))
        
    return ''.join(result[::-1]).lstrip('0') or '0'


# ---------------------------------------------------------------
# 2. TRADITIONAL MULTIPLICATION (Grade-School method)
#    Multiplies digit by digit and handles carries.
# ---------------------------------------------------------------
def traditional_multiply(x, y):
    # Remove leading zeros
    x = x.lstrip('0') or '0'
    y = y.lstrip('0') or '0'
    
    if x == '0' or y == '0':
        return '0'
        
    m, n = len(x), len(y)
    result = [0] * (m + n) # Max possible length
    
    # Multiply from right to left
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            mul = int(x[i]) * int(y[j])
            # Add to the correct position in the result array
            p1, p2 = i + j, i + j + 1
            total = mul + result[p2]
            
            result[p2] = total % 10
            result[p1] += total // 10
            
    # Convert list back to string
    res_str = ''.join(map(str, result)).lstrip('0')
    return res_str if res_str else '0'


# ---------------------------------------------------------------
# 3. KARATSUBA'S ALGORITHM (Divide & Conquer, 3 multiplications)
# ---------------------------------------------------------------
def karatsuba(x, y):
    # Remove leading zeros
    x = x.lstrip('0') or '0'
    y = y.lstrip('0') or '0'
    
    # Base case: if numbers are small, use traditional method
    if len(x) <= 2 or len(y) <= 2:
        return traditional_multiply(x, y)
        
    # Make both strings the same length
    n = max(len(x), len(y))
    half = n // 2
    
    # Pad with zeros on the left so the split is exact
    x = x.zfill(n)
    y = y.zfill(n)
    
    # Split into halves
    a = x[:-half]
    b = x[-half:]
    c = y[:-half]
    d = y[-half:]
    
    # 3 recursive multiplications (Karatsuba's magic)
    z1 = karatsuba(a, c)            # a * c
    z2 = karatsuba(b, d)            # b * d
    z3 = karatsuba(string_add(a, b), string_add(c, d)) # (a+b)*(c+d)
    
    # Combine: (z1 * 10^(2*half)) + ((z3 - z1 - z2) * 10^half) + z2
    mid_term = string_sub(string_sub(z3, z1), z2)
    
    # Append zeros (equivalent to multiplying by 10^half)
    part1 = z1 + ('0' * (2 * half))
    part2 = mid_term + ('0' * half)
    part3 = z2
    
    return string_add(string_add(part1, part2), part3)


# ---------------------------------------------------------------
# 4. MAIN DRIVER
# ---------------------------------------------------------------
if __name__ == "__main__":
    
    # ---------- PART A: Small visible demo ----------
    print("=" * 60)
    print("DEMO: 8-digit multiplication (both methods shown)")
    print("=" * 60)
    
    demo_x = "12345678"
    demo_y = "87654321"
    
    print(f"Number X: {demo_x}")
    print(f"Number Y: {demo_y}")
    
    demo_trad = traditional_multiply(demo_x, demo_y)
    demo_kar  = karatsuba(demo_x, demo_y)
    
    print(f"\nTraditional result: {demo_trad}")
    print(f"Karatsuba result:   {demo_kar}")
    print(f"Results match? -> {demo_trad == demo_kar}")
    
    # ---------- PART B: Timing table ----------
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON (Random Numbers)")
    print("=" * 60)
    print(f"{'Digits':>6} | {'Match?':>6} | {'Traditional (s)':>16} | {'Karatsuba (s)':>14}")
    print("-" * 60)
    
    # Test sizes requested in the lab (up to 1024 digits)
    sizes = [8, 16, 32, 64, 128, 256, 512, 1024]
    
    for n in sizes:
        # Generate random n-digit numbers (first digit 1-9 so no leading zero)
        x = str(random.randint(1, 9)) + ''.join(str(random.randint(0, 9)) for _ in range(n - 1))
        y = str(random.randint(1, 9)) + ''.join(str(random.randint(0, 9)) for _ in range(n - 1))
        
        # Time Traditional
        t0 = time.perf_counter()
        res_trad = traditional_multiply(x, y)
        t1 = time.perf_counter()
        
        # Time Karatsuba
        t2 = time.perf_counter()
        res_kar = karatsuba(x, y)
        t3 = time.perf_counter()
        
        match = (res_trad == res_kar)
        
        print(f"{n:>6} | {str(match):>6} | {t1 - t0:>16.6f} | {t3 - t2:>14.6f}")