# 1011. Capacity To Ship Packages Within D Days

class Solution(object):
    def shipWithinDays(self, weights, days):
        def check_days(s):
            sum = 0 
            count = 0
            for i in weights:
                if sum+i > s:
                    sum = 0 
                    count += 1
                sum = sum + i
            if count != days:
                return False
            else :
                return True
        if check_days(12):
            return 12

# a = Solution()
# print(a.shipWithinDays([1,2,3,4,5,6,7,8,9,10],5))

class Solution(object):
    def shipWithinDays(self, weights, days):

        left = max(weights)
        right = sum(weights)

        while left < right:

            mid = (left + right) // 2

            need = 1
            current = 0

            for w in weights:

                if current + w > mid:
                    need += 1
                    current = 0

                current += w

            if need <= days:
                right = mid
            else:
                left = mid + 1

        return left




                