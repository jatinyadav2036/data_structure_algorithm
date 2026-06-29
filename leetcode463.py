# 463. Island Perimeter

class Solution(object):
    def islandPerimeter(self, grid):
        n = len(grid)
        m = len(grid[0])
        perimeter = 0

        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    perimeter += 4

                    if i + 1 < n and grid[i + 1][j] == 1:
                        perimeter -= 2

                    if j + 1 < m and grid[i][j + 1] == 1:
                        perimeter -= 2

        return perimeter
    
# class Solution(object):
#     def islandPerimeter(self, grid):
#         n = len(grid)
#         m = len(grid[0])
#         perimeter = 0

#         for i in range(n):
#             for j in range(m):
#                 if grid[i][j] == 1:
#                     if i == 0 or grid[i-1][j] == 0:
#                         perimeter += 1
#                     if i == n-1 or grid[i+1][j] == 0:
#                         perimeter += 1
#                     if j == 0 or grid[i][j-1] == 0:
#                         perimeter += 1
#                     if j == m-1 or grid[i][j+1] == 0:
#                         perimeter += 1

#         return perimeter