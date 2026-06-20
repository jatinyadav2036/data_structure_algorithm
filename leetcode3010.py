# 3010. Divide an Array Into Subarrays With Minimum Cost I

class Solution(object):
    def minimumCost(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        c = nums.pop(0)
        min_val = min(nums)
        a = nums.pop(nums.index(min_val))
        min_val = min(nums)
        b = nums.pop(nums.index(min_val))
        return a + b + c
        

# class Solution(object):
#     def minimumCost(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: int
#         """
#         num= nums[1:]
#         num.sort()
#         return nums[0]+num[0]+num[1]