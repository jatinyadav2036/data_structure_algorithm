# 1572. Matrix Diagonal Sum

class Solution(object):
    def diagonalSum(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """
        count = 0
        for i in range(len(mat)):
            for j in range(len(mat)):
                if i == j or (i + j == len(mat) - 1):
                    count += mat[i][j]
        return count
    
    # class Solution(object):
    #     def diagonalSum(self, mat):
    #         s=0
    #         n=len(mat)
    #         for i in range(n):
    #             s+=mat[i][i]
    #             if (i,i)!=(i,n-i-1):
    #                 s+=mat[i][n-i-1]
    #         return s