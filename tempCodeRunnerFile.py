class Solution(object):
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