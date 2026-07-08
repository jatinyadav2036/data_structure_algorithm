# 605. Can Place Flowers

class Solution(object):
    def canPlaceFlowers(self, flowerbed, n):
        """
        :type flowerbed: List[int]
        :type n: int
        :rtype: bool
        """
        if n == 0 :
            return True
        if len(flowerbed) == 1:
            if flowerbed[0] == 0 and n == 1 :
                return True
            else:
                return False
        cnt = 0
        if flowerbed[0] == 0 and flowerbed[1] == 0 :
            flowerbed[0] = 1
            cnt += 1
            if cnt == n:
                return True
        for i in range(1,len(flowerbed)-1):
            if flowerbed[i-1] == 0 and flowerbed[i] == 0 and flowerbed[i+1] == 0:
                flowerbed[i] = 1
                cnt +=1 
                if cnt == n:
                    return True
        if flowerbed[-1] == 0 and flowerbed[-2] == 0:
            flowerbed[-1] = 1
            cnt += 1 
            if cnt == n:
                return True
        return False
        
        

# class Solution(object):
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