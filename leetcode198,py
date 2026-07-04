# 198. House Robber

class Solution(object):
    def rob(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        a = 0
        b = 0
        for i in nums:
            c = max(a,b+i)
            b = a 
            a = c
        return a
        