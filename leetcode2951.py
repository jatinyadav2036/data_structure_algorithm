# 2951. Find the Peaks
class Solution(object):
    def findPeaks(self, mountain):
        """
        :type mountain: List[int]
        :rtype: List[int]
        """
        a = []
        for i in range(1,len(mountain)-1):
            if (mountain[i-1] < mountain[i] and mountain[i] > mountain[i+1]):
                a.append(i)
        return a
        