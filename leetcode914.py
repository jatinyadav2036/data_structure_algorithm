# 914. X of a Kind in a Deck of Cards
from functools import reduce

class Solution(object):
    def hasGroupsSizeX(self, deck):
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
            
        hsh = {}
        for i in deck:
            hsh[i] = hsh.get(i, 0) + 1
            
        total_gcd = reduce(gcd, hsh.values())
        
        return total_gcd >= 2

s = Solution()
print(s.hasGroupsSizeX([1,1,2,2,2,2,3,3]))  