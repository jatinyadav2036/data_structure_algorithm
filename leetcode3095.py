# 3095. Shortest Subarray With OR at Least K I

class Solution(object):
    def minimumSubarrayLength(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        if k == 0:
            return 1

        bits = [0] * 32
        left = 0
        curr_or = 0
        ans = float('inf')

        for right in range(len(nums)):
            # Add nums[right]
            for b in range(32):
                if nums[right] & (1 << b):
                    bits[b] += 1
                    curr_or |= (1 << b)

            # Shrink window while OR >= k
            while left <= right and curr_or >= k:
                ans = min(ans, right - left + 1)

                # Remove nums[left]
                for b in range(32):
                    if nums[left] & (1 << b):
                        bits[b] -= 1
                        if bits[b] == 0:
                            curr_or &= ~(1 << b)
                left += 1

        return -1 if ans == float('inf') else ans