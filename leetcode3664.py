# 3664. Two-Letter Card Game

from collections import Counter

class Solution(object):
    def score(self, cards, x):
        cnt1 = [0] * 10
        cnt2 = [0] * 10
        both = 0

        for s in cards:
            if s[0] == x and s[1] == x:
                both += 1
            elif s[0] == x:
                cnt1[ord(s[1]) - ord('a')] += 1
            elif s[1] == x:
                cnt2[ord(s[0]) - ord('a')] += 1

        def solve(cnt, have):
            arr = sorted(cnt)
            total = sum(arr)

            if have >= total:
                return total

            remain = total - have

            if remain & 1:
                remain -= 1

            mx = arr[-1]
            other = total - mx

            internal = min(total // 2, other)

            return min(internal, remain // 2) + have

        ans = 0
        for i in range(both + 1):
            ans = max(ans, solve(cnt1, i) + solve(cnt2, both - i))

        return ans