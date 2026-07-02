# 3487. Maximum Unique Subarray Sum After Deletion

class Solution(object):
    def maxSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if max(nums) < 0 :
            return max(nums)
        sm = 0
        lst = list(set(nums))
        for i in lst:
            if i < 0 :
                continue
            sm += i
        return sm
        
# class Solution(object):
#     def maxSum(self, nums):
#         posNumSum = set([num for num in nums if num > 0])
#         return max(nums) if len(posNumSum) == 0 else sum(posNumSum)
#         """
#         :type nums: List[int]
#         :rtype: int
#         """

# class Solution(object):
#     def maxSum(self, nums):
#         if max(nums)<=0:
#             return max(nums)
#         a=[]
#         s=0
#         for i in nums:
#             if i>0 and i not in a:
#                 a.append(i)
#                 s+=i
#         return s