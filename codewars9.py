# Maximum Triplet Sum (Array Series #7)

def max_tri_sum(numbers):
    nums = set(numbers)
    n = list(nums)
    n.sort(reverse=True)
    sum = 0
    for i in range(3):
        sum += n[i]
    return sum

a = max_tri_sum([2,1,8,0,6,4,8,6,2,4])
print(a)
