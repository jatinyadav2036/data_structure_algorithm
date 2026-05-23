# Last digit of large number

def last_digit(n1, n2):
    if n2 == 0:
        return 1
    
    # Last digit cycles
    cycles = {
        0: [0],
        1: [1],
        2: [2, 4, 8, 6],
        3: [3, 9, 7, 1],
        4: [4, 6],
        5: [5],
        6: [6],
        7: [7, 9, 3, 1],
        8: [8, 4, 2, 6],
        9: [9, 1]
    }
    
    last = n1 % 10
    cycle = cycles[last]
    
    return cycle[(n2 - 1) % len(cycle)]