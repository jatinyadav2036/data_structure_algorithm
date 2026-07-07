class Solution(object):
#     def decrypt(self, code, k):
#         """
#         :type code: List[int]
#         :type k: int
#         :rtype: List[int]
#         """
#         ans=[0]*len(code)

#         if k==0:
#             return ans
        
#         start=1
#         end=k
#         current_val=0
        
#         if k<0:
#             start= len(code)-abs(k)
#             end= len(code)-1
#         for i in range(start,end+1):
#             current_val+=code[i]
        
#         for i in range(len(code)):
#             ans[i]=current_val
#             current_val-=code[start%len(code)]
#             current_val+=code[(end+1)%len(code)]
#             start+=1
#             end+=1
#         return ans