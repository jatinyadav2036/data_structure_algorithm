# 343. Integer Break

class Solution(object):
    def integerBreak(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 2 :
            return 1
        elif n == 3:
            return 2
        rem = n%3
        if rem == 0:
            return (3**(n//3))
        elif rem == 1:
            a = n//3 -1 
            return (3**(a)*4)
        else:
            return (3**(n//3)*2)
        
# class Solution(object):
#     def integerBreak(self, n):
#         if n == 2: return 1
#         if n == 3: return 2
#         product = 1
#         while n > 4:
#             product=product * 3
#             n=n-3
#         return product * n

s = Solution()
print(s.integerBreak(19))