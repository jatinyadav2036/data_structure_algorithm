# 1561. Maximum Number of Coins You Can Get

class Solution(object):
    def maxCoins(self, piles):
        piles.sort()
        sm = 0 
        i = len(piles) - 2
        while i >= len(piles) // 3:
            sm += piles[i]
            i -= 2
        return sm

# class Solution(object):
#     def maxCoins(self, piles):
#         piles.sort()
#         # Slices the array from the start of your zone to the end, skipping every 2nd element
#         return sum(piles[len(piles) // 3 :: 2])
