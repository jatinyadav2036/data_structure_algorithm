# 424. Longest Repeating Character Replacement

class Solution(object):
    def characterReplacement(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        count = {}
        left = 0
        max_freq = 0
        ans = 0

        for right in range(len(s)):
            count[s[right]] = count.get(s[right], 0) + 1

            # Maximum frequency character in current window
            max_freq = max(max_freq, count[s[right]])

            # If replacements needed are more than k
            while (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1

            ans = max(ans, right - left + 1)

        return ans
    class Solution(object):
        def characterReplacement(self, s, k):
            freq = [0] * 26
            left = 0
            maxf = 0
            ans = 0

            for right in range(len(s)):
                idx = ord(s[right]) - 65
                freq[idx] += 1

                if freq[idx] > maxf:
                    maxf = freq[idx]

                while right - left + 1 - maxf > k:
                    freq[ord(s[left]) - 65] -= 1
                    left += 1

                window = right - left + 1
                if window > ans:
                    ans = window

            return ans