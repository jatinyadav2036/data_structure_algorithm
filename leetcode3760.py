# 3760. Maximum Substrings With Distinct Start

class Solution(object):
    def maxDistinct(self, s):
        """
        :type s: str
        :rtype: int
        """
        sub_string = set(s)
        return len(sub_string)
        