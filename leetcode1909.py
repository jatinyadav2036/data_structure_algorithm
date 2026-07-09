# 1909. Remove One Element to Make the Array Strictly Increasing
class Solution(object):
    def canBeIncreasing(self, nums):
        removed = False

        for i in range(len(nums) - 1):
            if nums[i] >= nums[i + 1]:
                if removed:
                    return False
                removed = True

                if i > 0 and nums[i - 1] >= nums[i + 1]:
                    nums[i + 1] = nums[i]
        return True
    


