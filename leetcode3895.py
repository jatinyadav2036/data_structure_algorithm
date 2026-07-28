# 3895. Count Digit Appearances

class Solution(object):
    def countDigitOccurrences(self, nums, digit):
        def dig(n):
            cnt = 0
            while n > 0:
                temp = n % 10
                if temp == digit :
                    cnt += 1
                n = n // 10
            return cnt
        sm = 0
        for i in nums:
            sm += dig(i)
        return sm

# class Solution(object):
#     def countDigitOccurrences(self, nums, digit):
#         """
#         :type nums: List[int]
#         :type digit: int
#         :rtype: int
#         """
#         return str(nums).count(str(digit))