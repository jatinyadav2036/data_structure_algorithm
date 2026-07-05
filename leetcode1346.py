# 1346. Check If N and Its Double Exist

class Solution(object):
    def checkIfExist(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """
        if arr.count(0) >= 2 :
            return True
        for i in arr:
            if i % 2 == 0 and i //2 in arr and i != 0:
                return True
        return False
        

# class Solution(object):
#     def checkIfExist(self, arr):
#         seen = set()

#         for x in arr:
#             if 2 * x in seen or (x % 2 == 0 and x // 2 in seen):
#                 return True
#             seen.add(x)

#         return False