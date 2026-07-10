# 2760. Longest Even Odd Subarray With Threshold

class Solution(object):
    def longestAlternatingSubarray(self, nums, threshold):
        mx = 0
        for i in range(len(nums)):
            if nums[i] % 2 == 0 and nums[i] <= threshold:
                j = i + 1
                cnt = 1
                
                while j < len(nums):
                    if nums[j] <= threshold and nums[j] % 2 != nums[j - 1] % 2:
                        cnt += 1
                        j += 1
                    else:
                        break
                        
                if cnt > mx :
                    mx = cnt

        return mx
        
s = Solution()
print(s.longestAlternatingSubarray([2,10,5],7))



# class Solution(object):
#     def longestAlternatingSubarray(self, nums, threshold):
#         n = len(nums)
#         ans = 0
#         i = 0

#         while i < n:
#             if nums[i] % 2 or nums[i] > threshold:
#                 i += 1
#                 continue

#             j = i
#             while (j + 1 < n and
#                    nums[j + 1] <= threshold and
#                    nums[j] % 2 != nums[j + 1] % 2):
#                 j += 1

#             ans = max(ans, j - i + 1)
#             i = j + 1

#         return ans