# 665. Non-decreasing Array

class Solution(object):
    def checkPossibility(self, nums):
        cnt = 0
        for i in range(len(nums)-1):
            if nums[i] > nums[i+1]:
                cnt += 1
                if cnt > 1:
                    return False
                if i > 0 and nums[i - 1] > nums[i + 1]:
                    nums[i + 1] = nums[i] 
        return True



s = Solution()
print(s.checkPossibility([4,2,1]))