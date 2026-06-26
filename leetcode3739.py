# 3739. Count Subarrays With Majority Element II

class Solution(object):
    def countMajoritySubarrays(self, nums, target):
        n = len(nums)
        ans = 0

        for i in range(n):
            freq = 0
            for j in range(i, n):
                if nums[j] == target:
                    freq += 1
                if freq > (j - i + 1) // 2:
                    ans += 1

        return ans