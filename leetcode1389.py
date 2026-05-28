# 1389. Create Target Array in the Given Order

class Solution(object):
    def createTargetArray(self, nums, index):
        """
        :type nums: List[int]
        :type index: List[int]
        :rtype: List[int]
        """
        target = []
        for i,j in zip(nums,index):
            target.insert(j,i)

        return target