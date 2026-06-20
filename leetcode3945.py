# 3945. Digit Frequency Score

class Solution(object):
    def digitFrequencyScore(self, n):
        """
        :type n: int
        :rtype: int
        """
        b =  [int(d) for d in str(n)]
        l = set(b)
        s = 0
        a = 0
        for i in l :
            a  =  b.count(i)
            s += int(i)*int(a)
        return s
        
# class Solution(object):
#     def digitFrequencyScore(self, n):
#         score = 0

#         while n > 0:
#             digit = n % 10
#             score += digit
#             n //= 10

#         return score    