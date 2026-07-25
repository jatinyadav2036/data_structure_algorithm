# 139. Word Break

class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: bool
        """
        # Convert list to a set for O(1) membership lookups
        word_set = set(wordDict)
        
        # dp[i] means s[0:i] can be segmented
        dp = [False] * (len(s) + 1)
        dp[0] = True  # Base case: empty string
        
        # Iterate through all ending positions of substrings
        for i in range(1, len(s) + 1):
            # Check all possible split points before 'i'
            for j in range(i):
                # If s[0:j] is valid AND s[j:i] is in the dictionary
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break  # Found a valid segmentation for dp[i], move to next i
                    
        return dp[len(s)]
