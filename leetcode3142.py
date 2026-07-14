# 3142. Check if Grid Satisfies Conditions

class Solution(object):
    def satisfiesConditions(self, grid):
        m, n = len(grid), len(grid[0])

        for i in range(m):
            for j in range(n):
                # Check cell below
                if i + 1 < m and grid[i][j] != grid[i + 1][j]:
                    return False

                # Check cell to the right
                if j + 1 < n and grid[i][j] == grid[i][j + 1]:
                    return False

        return True