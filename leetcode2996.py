# 2996. Smallest Missing Integer Greater Than Sequential Prefix Sum

class Solution(object):
    def missingInteger(self, nums):
        i = 0
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1] + 1:
                i -= 1
                break

        sm = sum(nums[:i + 1])

        while sm in nums:
            sm += 1
        return sm


s = Solution()
print(s.missingInteger([3,4,5,1,12,14,13]))