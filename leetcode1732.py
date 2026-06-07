# 1732. Find the Highest Altitude

class Solution(object):
    def largestAltitude(self, gain):
        """
        :type gain: List[int]
        :rtype: int
        """
        alt = [0]
        s = 0
        for i in gain :
            s += i
            alt.append(s)

        return max(alt)