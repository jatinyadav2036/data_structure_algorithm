# 1470. Shuffle the Array

class Solution(object):
    def shuffle(self, nums, n):
        """
        :type nums: List[int]
        :type n: int
        :rtype: List[int]
        """
        a =[]
        left = nums[:n]
        right = nums[n:]
        for i in range(n):
            a.append(left[i])
            a.append(right[i])
        return a
    

# class Solution(object):
#     def shuffle(self, nums, n):
#         l = 0
#         res =[]
#         while n < len(nums):
#             res.append(nums[l])
#             res.append(nums[n])
#             l +=1
#             n +=1
#         return res