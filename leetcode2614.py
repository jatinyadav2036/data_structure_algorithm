# 2614. Prime In Diagonal

class Solution(object):
    def diagonalPrime(self, nums):
        def is_prime(n):
            if n <= 1 :
                return False
            if n == 2 :
                return True
            if n % 2 == 0 :
                return False
            for i in range(3,int(n**0.5)+1,2):
                if n % i == 0 :
                    return False
            return True
        mx_prime = 0
        for i in range(len(nums)):
            if is_prime(nums[i][i]) :
                val = nums[i][i]
                if mx_prime < val:
                    mx_prime = val
            if is_prime(nums[i][len(nums) - i - 1]):
                val = nums[i][len(nums) - i - 1]
                if mx_prime < val:
                    mx_prime = val
        return mx_prime
        
s = Solution()
print(s.diagonalPrime([[1,2,3],[5,6,7],[9,10,11]]))