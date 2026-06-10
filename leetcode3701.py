# 3701. Compute Alternating Sum

class Solution(object):
    def alternatingSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        even = 0
        odd = 0 
        for i in range(len(nums)):
            if i % 2 == 0 :
                even += nums[i]
            else:
                odd += nums[i]

        return even - odd

# class Solution(object):
#     def alternatingSum(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: int
#         """
#         s=0
#         for i in nums[::2]:
#             s+=i
#         for i in nums[1::2]:
#             s-=i
#         return s