class Solution(object):
#     def distMoney(self, money, children):
#         if money < children:
#             return -1

#         money -= children
#         ans = min(money // 7, children)

#         money -= ans * 7
#         children -= ans

#         if children == 0 and money > 0:
#             ans -= 1
#         elif children == 1 and money == 3:
#             ans -= 1

#         return ans