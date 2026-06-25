# 1920. Build Array from Permutation

class Solution(object):
    def buildArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        lst =[]
        for i in range(len(nums)):
            lst.append(nums[nums[i]])

        # for i in nums:
        #     lst.append(nums[i])

        return lst
        