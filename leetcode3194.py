# 3194. Minimum Average of Smallest and Largest Elements

# class Solution(object):
#     def minimumAverage(self, nums):
#         nums.sort()
#         avg= []

#         for i in range(len(nums)/2) :
#             avg.append((float)(nums[i] + nums[len(nums) - i - 1]) / 2)
        
#         return min(avg)

class Solution(object):
    def minimumAverage(self, nums):
        """
        :type nums: List[int]
        :rtype: float
        """
        average = []
        min_value,max_value = 0,0
        while len(nums)!=0:
            max_value = nums.pop(nums.index(max(nums)))
            min_value = nums.pop(nums.index(min(nums)))
            average.append((max_value+min_value)/2.0)
        return min(average)