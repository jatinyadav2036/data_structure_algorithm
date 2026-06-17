# 2215. Find the Difference of Two Arrays

class Solution(object):
    def findDifference(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[List[int]]
        """
        a = []
        b = []
        for i in nums1:
            if i not in nums2:
                a.append(i)
        for j in nums2:
            if j not in nums1:
                b.append(j)
        c = list(set(a))
        d = list(set(b))
        return [c,d]
    
# class Solution(object):
#     def findDifference(self, nums1, nums2):
#         set1, set2 = set(nums1), set(nums2) 
#         return [list(set1 - set2), list(set2 - set1)] 