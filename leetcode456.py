# 456. 132 Pattern

class Solution(object):
    def find132pattern(self, nums):
        stack = []
        third = float('-inf')

        for i in reversed(nums):
            if i < third :
                return True
            while stack and i > stack[-1]:
                third = stack.pop()
            stack.append(i)
        return False
                