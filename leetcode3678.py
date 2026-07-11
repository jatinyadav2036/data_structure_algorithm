# 3678. Smallest Absent Positive Greater Than Average

class Solution(object):
    def smallestAbsent(self, nums):

        avg = sum(nums) / float(len(nums))
        
        candidate = max(1, int(avg) + 1)
        
        num_set = set(nums)
        
        while candidate in num_set:
            candidate += 1
            
        return candidate
