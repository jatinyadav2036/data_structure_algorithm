# 3783. Mirror Distance of an Integer

class Solution(object):
    def mirrorDistance(self, n):
        """
        :type n: int
        :rtype: int
        """
        def reverse_integer(x):
            # Handle the negative sign flag
            sign = -1 if x < 0 else 1
            
            # Convert absolute value to string, reverse it with slicing [::-1], and convert back to int
            reversed_x = sign * int(str(abs(x))[::-1])
            
            # LeetCode requirement: Check for 32-bit signed integer overflow limits
            if reversed_x < -2**31 or reversed_x > 2**31 - 1:
                return 0
                
            return reversed_x
        return abs(n - reverse_integer(n))