# 202. Happy Number

class Solution(object):
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        def sqr_sum(num):
            s = 0
            while num > 0:
                temp = num % 10 
                s += temp **2
                num = num // 10
            return s
        seen = set()
        while n > 0:
            tem = sqr_sum(n)
            if tem == 1 :
                return True
            if tem in seen:
                return False
            seen.add(tem)
            n = tem
        return False