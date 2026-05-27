# 1480. Running Sum of 1d Array

class Solution(object):
    def runningSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        a = []
        sum = 0
        for i in nums:
            sum += i
            a.append(sum)

        return a