# 1013. Partition Array Into Three Parts With Equal Sum

class Solution(object):
    def canThreePartsEqualSum(self, arr):
        total = sum(arr)

        if total % 3 != 0:
            return False

        target = total // 3
        curr = 0
        count = 0

        # Stop before the last element so the third part is non-empty
        for i in range(len(arr) - 1):
            curr += arr[i]
            if curr == target:
                count += 1
                curr = 0
                if count == 2:
                    return True

        return False