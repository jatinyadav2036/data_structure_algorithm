# 593. Valid Square

class Solution(object):
    def validSquare(self, p1, p2, p3, p4):
        """
        :type p1: List[int]
        :type p2: List[int]
        :type p3: List[int]
        :type p4: List[int]
        :rtype: bool
        """
        def distance(a1,b1):
            return (( b1[0] - a1[0] ) **2  + ( b1[1] - a1[1] ) **2 ) 
        lst = []
        lst.append(distance(p1,p2))
        lst.append(distance(p1,p3))
        lst.append(distance(p1,p4))
        lst.append(distance(p2,p3))
        lst.append(distance(p2,p4))
        lst.append(distance(p3,p4))
        # s = set(lst)
        # if len(s) == 2:
        #     return True
        # return False
        lst.sort()

        if (
            lst[0] > 0 and
            lst[0] == lst[1] == lst[2] == lst[3] and
            lst[4] == lst[5] and
            lst[4] == 2 * lst[0]
        ):
            return True
        return False

# class Solution(object):
#     def validSquare(self, p1, p2, p3, p4):
#         """
#         :type p1: List[int]
#         :type p2: List[int]
#         :type p3: List[int]
#         :type p4: List[int]
#         :rtype: bool
#         """
#         def dist_sq(pt1, pt2):
#             return (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2
            
#         # Calculate distances for all 6 possible pairs
#         distances = {
#             dist_sq(p1, p2), dist_sq(p1, p3), dist_sq(p1, p4),
#             dist_sq(p2, p3), dist_sq(p2, p4),
#             dist_sq(p3, p4)
#         }
        
#         # Valid square has exactly 2 unique distances (sides & diagonals) and no 0 distance
#         return len(distances) == 2 and 0 not in distances