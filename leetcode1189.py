# 1189. Maximum Number of Balloons

class Solution(object):
    def maxNumberOfBalloons(self, text):
        """
        :type text: str
        :rtype: int
        """
        s = set(text)
        d = {'b': 0, 'a': 0, 'l': 0, 'o': 0, 'n': 0}
        c = 0
        for i in s:
            if i == 'b' or i == 'a' or i == 'l' or i == 'o' or i == 'n' :
                c = text.count(i)
                if i == 'l' or i =='o':
                    d[i] = c//2
                else:
                    d[i] = c
        return min(d.values())
        