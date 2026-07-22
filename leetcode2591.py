# 2591. Distribute Money to Maximum Children

class Solution(object):
    def distMoney(self, money, children):
        # Check if every children can get money or not
        #  Minus no. of children from money to get every children 1 dollar
        money -= children
        if money < 0:
            return -1
        # give children 8 dollars and count them
        cnt = 0
        for i in range(children):
            if money >= 7 :
                money -= 7
                cnt += 1
        # if only one children and get 4 dollar then minus 1 from count
        if money == 3 and cnt + 1 == children:
            cnt -= 1
        # after every children get 8 dollar and money remains then subtract 1 from count
        if cnt == children and money > 0:
            cnt -= 1
        return cnt
        

s = Solution()
print(s.distMoney(8,8))

# class Solution(object):
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