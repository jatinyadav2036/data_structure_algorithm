def sum_of_intervals(intervals):
    intervals = sorted(intervals)
    t = 0
    a,b = intervals[0]
    for i,j in intervals[1:]:
        if i <= b :
            b = max(b,j)
        else :
            t += b - a
            a,b = i,j
    return t + (b-a)