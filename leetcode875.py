# 875 Koko Eating Bananas
# import math
# class Solution(object):
#     def minEatingSpeed(self, piles, h):
        # """
        # :type piles: List[int]
        # :type h: int
        # :rtype: int
        # """
        # piles.sort()
        # count = 0
        # mid = (piles[0] + piles[-1]) // 2
        # i = 0

        # while i <= len(piles)-1:
        #     count = count + math.ceil(piles[i]/mid)
        #     i += 1
         
        # while count <= h :
        #     mid -=1
        #     count = 0 
        #     j = 0
        #     while j <= len(piles)-1:
        #         count = count + math.ceil(piles[j]/mid)
        #         j += 1

        # while count > h :
        #     mid +=1
        #     count = 0 
        #     k = 0
        #     while k <= len(piles)-1:
        #         count = count + math.ceil(piles[k]/mid)
        #         k += 1
        # return mid


class Solution(object):
    def minEatingSpeed(self, piles, h):
        def can_finish(k):
            hours = 0
            for p in piles:
                hours += (p + k - 1) // k
                if hours > h:
                    return False
            return True

        left, right = 1, max(piles)

        while left < right:
            mid = (left + right) // 2
            if can_finish(mid):
                right = mid
            else:
                left = mid + 1

        return left