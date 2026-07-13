# 3364. Minimum Positive Sum Subarray 

class Solution(object):
    def minimumSumSubarray(self, nums, l, r):
        """
        :type nums: List[int]
        :type l: int
        :type r: int
        :rtype: int
        """
        n = len(nums)
        ans = float('inf')

        for i in range(n):
            curr_sum = 0
            for j in range(i, n):
                curr_sum += nums[j]
                length = j - i + 1

                if length > r:
                    break

                if length >= l and curr_sum > 0:
                    ans = min(ans, curr_sum)

        return ans if ans != float('inf') else -1