# 2221. Find Triangular Sum of an Array

class Solution(object):
    def triangularSum(self, nums):
        if len(nums) == 1:
            return nums[0]
        while True:
            arr = []
            for i in range(len(nums)-1):
                arr.append((nums[i]+nums[i+1])%10)
            if len(arr) == 1:
                return arr[0]
            nums[:] = arr
            
            
            
        