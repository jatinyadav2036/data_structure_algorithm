# 3731. Find Missing Elements

class Solution(object):
    def findMissingElements(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        nums.sort()
        n = nums[-1] - nums[0]
        n += 3
        m = []
        for i in range(n):
            if nums[i] == nums[-1]:
                break
            elif nums[i] + 1 != nums[i+1] :
                nums.insert(i+1,(nums[i]+1))
                m.append(nums[i]+1)
        return m

s = Solution()
print(s.findMissingElements([5,1]))

# class Solution(object):
#     def findMissingElements(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: List[int]
#         """
#         start, end = min(nums), max(nums)

#         seen = set(nums)
#         result = []

#         for i in range(start + 1, end):
#             if i not in seen:
#                 result.append(i)

#         return result