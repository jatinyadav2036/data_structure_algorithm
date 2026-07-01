# 326. Power of Three

class Solution(object):
    def isPowerOfThree(self, n):
        """
        :type n: int
        :rtype: bool
        """
        if n == 1 or n == 3:
            return True
        if n == 0 or n % 3 != 0 :
            return False
        return self.isPowerOfThree(n//3)

# class Solution(object):
#     def isPowerOfThree(self, n):
#         return n > 0 and 1162261467 % n == 0