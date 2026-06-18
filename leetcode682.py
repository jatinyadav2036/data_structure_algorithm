# 682. Baseball Game

class Solution(object):
    def calPoints(self, operations):
        """
        :type operations: List[str]
        :rtype: int
        """
        r = []
        s = 0
        for i in operations:
            if i == "C":
                r.pop()
            elif i == "D":
                r.append(int(r[-1]) * 2)
            elif i == "+":
                r.append(int(r[-1])+int(r[-2]))
            else:
                r.append(i)
        for j in r:
            s  = s + int(j)
        return s