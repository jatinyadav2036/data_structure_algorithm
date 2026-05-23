# 3925. Concatenate Array With Reverse

# class Solution(object):
#     def concatWithReverse(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: List[int]
#         """
#         l=[]
#         l[:]=nums
#         for i in range(len(nums)-1,-1,-1):
#             l.append(nums[i])
#         return l

class Solution(object):
    def concatWithReverse(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        a =[]
        for i in nums:
            a.append(i)
        s = nums[::-1]
        for j in s:
            a.append(j)
        return a