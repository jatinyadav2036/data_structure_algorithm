# 21. Maxie and Minnie

def swap(number):
    digits = list(str(number))
    n = len(digits)
    
    max_digits = list(digits)
    for i in range(n):
        best_digit = max_digits[i]
        best_idx = i
        for j in range(n - 1, i, -1):
            if max_digits[j] > best_digit:
                best_digit = max_digits[j]
                best_idx = j
        if best_idx != i:
            max_digits[i], max_digits[best_idx] = max_digits[best_idx], max_digits[i]
            break
    maxie = int("".join(max_digits))
    
    min_digits = list(digits)
    for i in range(n):
        best_digit = min_digits[i]
        best_idx = i
        for j in range(n - 1, i, -1):
            if i == 0 and min_digits[j] == '0':
                continue
            if min_digits[j] < best_digit:
                best_digit = min_digits[j]
                best_idx = j
        if best_idx != i:
            min_digits[i], min_digits[best_idx] = min_digits[best_idx], min_digits[i]
            break
    minnie = int("".join(min_digits))
    
    return maxie, minnie
