class Solution(object):
#     def canPlaceFlowers(self, flowerbed, n):
#         if n == 0:
#             return True

#         m = len(flowerbed)

#         for i in range(m):
#             if (flowerbed[i] == 0 and
#                 (i == 0 or flowerbed[i - 1] == 0) and
#                 (i == m - 1 or flowerbed[i + 1] == 0)):

#                 flowerbed[i] = 1
#                 n -= 1

#                 if n == 0:
#                     return True

#         return False