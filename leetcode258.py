# 258. Add Digits

class Solution(object):
    def addDigits(self, num):
        """
        :type num: int
        :rtype: int
        """
        def s(a):
            i = 0 
            b = 0
            while i < len(a):
                b += a[i]
                i += 1
            return b
        p = list(map(int, str(num)))
        while len(p) != 1:
            p = s(p)
            p = list(map(int, str(p)))
        return p[0]
        
# class Solution(object):
#     def addDigits(self, num):
#         if num == 0:
#             return (0)
#         elif num % 9 == 0:
#             return 9
#         else:
#             return num%9