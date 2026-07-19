# 1331. Rank Transform of an Array

class Solution(object):
    def arrayRankTransform(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """
        # Sort unique values
        sorted_unique = sorted(set(arr))
        
        # Map each value to its rank
        rank = {}
        for i, num in enumerate(sorted_unique):
            rank[num] = i + 1
        
        # Replace each element with its rank
        return [rank[num] for num in arr]