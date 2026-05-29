# 3162. Find the Number of Good Pairs I

class Solution(object):
    def numberOfPairs(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: int
        """
        count = 0 
        for i in nums1:
            for j in nums2:
                if i % (j*k) == 0:
                    count += 1

        return count