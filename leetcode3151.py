# 3151. Special Array I

class Solution(object):
    def isArraySpecial(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        if len(nums) == 1 :
            return True

        i = 0
        j = 1
        while j < len(nums):
            if (nums[i] % 2 == 0 and nums[j] % 2 == 0) or (nums[i] % 2 != 0 and nums[j] % 2 != 0):
                return False
            i += 1
            j += 1
        return True
    
# class Solution(object):
#     def isArraySpecial(self, nums):
#         if len(nums)==1:
#             return True
#         for i in range(len(nums)-1):
#             if nums[i]%2==nums[i+1]%2:
#                 return False
#         return True 