#122. Best Time to Buy and Sell Stock II

class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        n = len(prices)
        res = 0
        for i,j in zip(range(0,n-1),range(1,n)):
            if prices[i] < prices[j]:
                res += prices[j] - prices[i]

        return res
        