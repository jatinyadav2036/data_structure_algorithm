# 2765. Longest Alternating Subarray

class Solution(object):
    def alternatingSubarray(self, nums):
        max_len = -1
        current_len = -1
        
        for i in range(1, len(nums)):
            diff = nums[i] - nums[i - 1]
            
            if current_len != -1:
                expected_diff = 1 if current_len % 2 == 1 else -1
                if diff == expected_diff:
                    current_len += 1
                    max_len = max(max_len, current_len)
                else:
                    current_len = 2 if diff == 1 else -1
            elif diff == 1:
                current_len = 2
                max_len = max(max_len, current_len)
                
        return max_len
