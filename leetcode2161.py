# 2161. Partition Array According to Given Pivot

class Solution:
    def pivotArray(self, nums, pivot):
        less = [x for x in nums if x < pivot]
        equal = [x for x in nums if x == pivot]
        greater = [x for x in nums if x > pivot]

        return less + equal + greater