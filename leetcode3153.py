# 3153. Sum of Digit Differences of All Pairs

class Solution(object):
    def sumDigitDifferences(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # Convert integers to string arrays for column extraction
        lst = [str(i) for i in nums]
        transposed = list(map(list, zip(*lst)))
        
        total_diff = 0
        N = len(nums)
        
        # Process one digit position (column) at a time
        for col in transposed:
            # Count the frequency of each digit (0-9) in this column
            counts = {}
            for digit in col:
                counts[digit] = counts.get(digit, 0) + 1
            
            # Calculate differences using frequencies
            col_diff = 0
            for digit, k in counts.items():
                col_diff += k * (N - k)
            
            # Divide by 2 because each pair difference was counted twice
            total_diff += col_diff // 2
            
        return total_diff

# Test Case
s = Solution()
print(s.sumDigitDifferences([50, 48, 28]))  # Output: 5
