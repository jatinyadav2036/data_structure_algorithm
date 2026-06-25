# Merge Sort

num = [32,56,82,54,45,28,94,14]

def merge_sort(nums,low,high):
    if low >= high:
        return
    mid = (low + high ) // 2
    merge_sort(nums,low,mid)
    merge_sort(nums,mid+1,high)
    return merge(nums,low,mid,high)

def merge(nums,low,mid , high):
    temp = []
    left = low
    right = mid + 1
    while(left<=mid and right<=high):
        if nums[left] <= nums[right]:
            temp.append(nums[left])
            left += 1
        else:
            temp.append(nums[right])
            right += 1

    while left <= mid:
        temp.append(nums[left])
        left +=1 
    
    while right  <= high:
        temp.append(nums[right])
        right += 1

    for i in range(low,high+1):
        nums[i] = temp[i-low]
    return nums

print(merge_sort(num,0,len(num)-1))



# Quick Sort

def quick_sort(nums,low,high):
    if low < high :
        partition_index = quick(nums,low,high)
        quick_sort(nums,low,partition_index-1)
        quick_sort(nums,partition_index+1 , high)
        return nums


def quick(nums,low,high):
    pivot = nums[low]
    i = low
    j = high

    while i < j:
        while i <= high and nums[i] <= pivot:
            i += 1
        while j >= low and nums[j] > pivot:
            j -= 1
        if i < j:
            nums[i], nums[j] = nums[j] , nums[i]
        
    nums[low] , nums[j] = nums[j] , nums[low]
    return j
print(quick_sort(num,0,len(num)-1))

        
    
