# 10 Stalin Sort
def stalin_sort(arr):
    # The Party demands order. Provide it.
    # Hint: print("Расстрелять!") for each eliminated element
    n = len(arr)
    if n ==0:
        return None
    # for i in range(1,n):
    #     if arr[i] < arr[i-1]:
    #         lst.append(arr[i])
    i = 1
    while i < n:
        if arr[i] < arr[i-1]:
            arr.pop(i)
            n -= 1
        else:
            i += 1


    return arr

print(stalin_sort([5, 3, 1, 2, 4]))
