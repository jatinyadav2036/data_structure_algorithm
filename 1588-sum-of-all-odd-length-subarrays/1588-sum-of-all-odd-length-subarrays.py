class Solution(object):
    def sumOddLengthSubarrays(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """
        s = 0
        subarrays = [arr[i:j] for i in range(len(arr)) for j in range(i + 1, len(arr) + 1)]
        for i in  subarrays:
            if len(i)%2 != 0:
                s += sum(i)
        return s

