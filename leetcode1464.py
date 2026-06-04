# 1464. Maximum Product of Two Elements in an Array

class Solution(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        a = nums.pop(nums.index(max(nums)))
        b = nums.pop(nums.index(max(nums)))

        return (a-1)*(b-1)
        