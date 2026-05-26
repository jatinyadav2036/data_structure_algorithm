# 1431. Kids With the Greatest Number of Candies

class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        """
        :type candies: List[int]
        :type extraCandies: int
        :rtype: List[bool]
        """
        b = []
        m = max(candies)
        for i in candies:
            if (i+extraCandies) >= m:
                b.append(True)
            else:
                b.append(False)

        return b