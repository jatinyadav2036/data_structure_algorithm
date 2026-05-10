# 73 Set Matrix Zero
class Solution(object):
    def setZeroes(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        r = len(matrix)
        c = len(matrix[0])
        lst = []
        for i in range(r):
            for j in range(c):
                if matrix[i][j] == 0 :
                    lst.append((i,j))

        for k,l in lst:
            matrix[k] = [0] * c
            for m in range(r):
                matrix[m][l] = 0
    
        return matrix
        