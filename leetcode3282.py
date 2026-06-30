# 3282. Reach End of Array With Max Score


class Solution(object):
    def findMaximumScore(self, nums):
        n = len(nums)
        ans = 0
        best = nums[0]

        for i in range(1, n):
            ans += best
            if nums[i] > best:
                best = nums[i]

        return ans
    
    # def findMaximumScore(self, nums):
    #     """
    #     :type nums: List[int]
    #     :rtype: int
    #     """
    #     res = ma = 0
    #     for a in nums:
    #         res += ma
    #         ma = max(ma, a)
    #     return res