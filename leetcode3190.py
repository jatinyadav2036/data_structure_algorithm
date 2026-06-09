# 3190. Find Minimum Operations to Make All Elements Divisible by Three

class Solution(object):
    def minimumOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        count = 0 
        for i in nums:
            if i%3 == 0 :
                continue
            else:
                count += 1

        return count
        