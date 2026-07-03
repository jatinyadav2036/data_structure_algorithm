# 1037. Valid Boomerang

class Solution(object):
    def isBoomerang(self, points):
        """
        :type points: List[List[int]]
        :rtype: bool
        """
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]
    
        return (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) != 0
    

# class Solution(object):
#     def isBoomerang(self, points):
#         # Unpack everything in a single, clean line
#         (x1, y1), (x2, y2), (x3, y3) = points

#         # Your optimal slope check
#         return (y2 - y1) * (x3 - x1) != (y3 - y1) * (x2 - x1)
