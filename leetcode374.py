# 374. Guess Number Higher or Lower

# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num):

class Solution(object):
    def guessNumber(self, n):
        left = 0
        right = n 
        while True :
            mid  = ( left + right ) // 2 
            result = guess(mid)
            if result == 0:
                return mid
            elif result == -1:
                right = mid -1
            else:
                left = mid + 1
                 