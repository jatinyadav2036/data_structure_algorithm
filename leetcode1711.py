# 1711. Count Good Meals

class Solution(object):
    def countPairs(self, deliciousness):
        MOD = 10**9 + 7
        count = {}
        ans = 0

        for x in deliciousness:
            power = 1
            while power <= 1 << 21:
                ans += count.get(power - x, 0)
                power <<= 1
            count[x] = count.get(x, 0) + 1

        return ans % MOD
    

# class Solution(object):
#     def countPairs(self, deliciousness):
#         """
#         :type deliciousness: List[int]
#         :rtype: int
#         """
#         MOD = 10**9 + 7
#         max_val = max(deliciousness)
#         max_sum = max_val * 2
#         power_of_twos = [1 << i for i in range(22)] 
        
#         count = defaultdict(int)
#         res = 0

#         for val in deliciousness:
#             for target in power_of_twos:
#                 complement = target - val
#                 if complement in count:
#                     res += count[complement]
#                     res %= MOD
#             count[val] += 1
        
#         return res