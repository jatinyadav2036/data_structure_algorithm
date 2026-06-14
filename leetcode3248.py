# 3248. Snake in Matrix
class Solution(object):
    def finalPositionOfSnake(self, n, commands):
        """
        :type n: int
        :type commands: List[str]
        :rtype: int
        """
        k,j = 0,0
        for i in range(len(commands)):
            if commands[i] == 'RIGHT':
                j += 1
            elif commands[i] == 'LEFT':
                j -= 1
            elif commands[i] == 'DOWN':
                k += 1
            elif commands[i] == 'UP':
                k -= 1
        return (k*n) + j
        
s = Solution()
print(s.finalPositionOfSnake(3,["DOWN","RIGHT","UP"]))