# 2828. Check if a String Is an Acronym of Words

class Solution(object):
    def isAcronym(self, words, s):
        """
        :type words: List[str]
        :type s: str
        :rtype: bool
        """
        l = []
        for i in words:
            l.append(i[0])

        a = "".join(l)
        return s == a

