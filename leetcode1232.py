# 1232. Check If It Is a Straight Line

class Solution(object):
    def checkStraightLine(self, coordinates):
        """
        :type coordinates: List[List[int]]
        :rtype: bool
        """
        # Extract initial reference point coordinates
        x0, y0 = coordinates[0]
        x1, y1 = coordinates[1]
        
        # Precompute the dx and dy of our base reference vector
        dx1 = x1 - x0
        dy1 = y1 - y0
        
        # Iterate through all remaining points to verify collinearity
        for i in range(2, len(coordinates)):
            x_i, y_i = coordinates[i]
            dx_i = x_i - x0
            dy_i = y_i - y0
            
            # Execute 2D cross product: dx1 * dy_i - dy1 * dx_i
            # If the result is not zero, the points are not collinear
            if dx1 * dy_i - dy1 * dx_i != 0:
                return False
                
        return True
