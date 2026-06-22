# 20. Next bigger number with the same digits

def next_bigger(n):
    d = list(str(n))

    # Find pivot
    i = len(d) - 2
    while i >= 0 and d[i] >= d[i + 1]:
        i -= 1

    if i < 0:
        return -1

    # Find smallest digit to the right that is bigger than pivot
    j = len(d) - 1
    while d[j] <= d[i]:
        j -= 1

    # Swap
    d[i], d[j] = d[j], d[i]

    # Sort suffix
    d[i + 1:] = sorted(d[i + 1:])

    return int("".join(d))