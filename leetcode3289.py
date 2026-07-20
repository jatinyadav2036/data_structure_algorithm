# 3289. The Two Sneaky Numbers of Digitville

class Solution(object):
    def getSneakyNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        freq = {}
        arr = []
        for i in nums:
            freq[i] = freq.get(i,0) + 1
            if freq[i] == 2:
                arr.append(i)
        return arr
        