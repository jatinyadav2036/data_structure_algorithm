# 3200. Maximum Height of a Triangle


class Solution(object):
    def maxHeightOfTriangle(self, red, blue):
        """
        :type red: int
        :type blue: int
        :rtype: int
        """
        def build(r, b, start_red):
            height = 0
            row = 1
            while True:
                if (row % 2 == 1) == start_red:
                    if r < row:
                        break
                    r -= row
                else:
                    if b < row:
                        break
                    b -= row
                height += 1
                row += 1
            return height

        return max(build(red, blue, True), build(red, blue, False))