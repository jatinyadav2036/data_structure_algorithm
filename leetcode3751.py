# 3751. Total Waviness of Numbers in Range I

class Solution(object):
    def totalWaviness(self, num1, num2):
        arr = range(num1,num2+1)
        sm= 0
        def wave(n):
            a = list(str(n))
            if len(a) < 3:
                return 0
            cnt = 0
            for i in range(1,len(a)-1):
                if a[i-1] < a[i] > a[i+1] or a[i-1] > a[i] < a[i+1]:
                    cnt += 1
            return cnt
        for j in arr:
            sm += wave(j)
        return sm
s = Solution()
print(s.totalWaviness(120,130))