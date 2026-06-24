# Selection Sorting

lst = [56,86,46,67,64,93,23,34]
n = len(lst)

# for i in range(n-1):
#     for j in range(i,n):
#         if lst[i] > lst[j]:
#             lst[i] , lst[j] = lst[j] , lst[i]

print(lst)

# Bubble Sorting

# for _ in lst:
#     for i in range(n-1):
#         if lst[i] > lst[i+1]:
#             lst[i] , lst[i+1] = lst[i+1] , lst[i]

for i in range(n-1,-1,-1):
    didSwap = 0
    for j in range(i):
        if lst[j] > lst[j+1]:
             lst[i] , lst[j] = lst[j] , lst[i]
             didSwap = 1
    if didSwap == 0:
        break

print(lst)
