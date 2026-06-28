# 1282. Group the People Given the Group Size They Belong To

class Solution(object):
    def groupThePeople(self, groupSizes):
        """
        :type groupSizes: List[int]
        :rtype: List[List[int]]
        """
        groups = {}
        ans = []

        for i, size in enumerate(groupSizes):
            if size not in groups:
                groups[size] = []

            groups[size].append(i)

            if len(groups[size]) == size:
                ans.append(groups[size])
                groups[size] = []

        return ans