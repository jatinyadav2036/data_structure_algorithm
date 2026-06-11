# 2965. Find Missing and Repeated Values

import numpy as np

class Solution(object):
    def findMissingAndRepeatedValues(self, grid):
        n = len(grid)

        matrix = np.array(grid).flatten()

        unique, counts = np.unique(matrix, return_counts=True)

        repeated = unique[counts > 1][0]

        expected = np.arange(1, n * n + 1)

        missing = np.setdiff1d(expected, unique)[0]

        return [int(repeated), int(missing)]
    

# class Solution(object):
#     def findMissingAndRepeatedValues(self, grid):
#         n=len(grid)
#         set_=set()
#         repeated=-1
#         for row in grid:
#             for num in row:
#                 if num in set_:
#                     repeated=num
#                 set_.add(num)
        
#         missing=-1
#         for num in range(1,n*n+1):
#             if num not in set_:
#                 missing=num
#                 break

#         return[repeated,missing]