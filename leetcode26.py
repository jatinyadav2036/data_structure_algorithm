# 26. Remove Duplicates from Sorted Array

class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0

        i = 1  # Position for next unique element

        for j in range(1, len(nums)):
            if nums[j] != nums[i - 1]:
                nums[i] = nums[j]
                i += 1

        return i