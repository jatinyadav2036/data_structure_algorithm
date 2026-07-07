# 1652. Defuse the Bomb

class Solution(object):
    def decrypt(self, code, k):
        """
        :type code: List[int]
        :type k: int
        :rtype: List[int]
        """
        decode = []
        if k == 0:
            return [0]*len(code)
        if k > 0 :
            for i in range(len(code)):
                sm = 0
                for j in range(i+1,i+k+1):
                    circular_index =  j % len(code) 
                    sm += code[circular_index]
                decode.append(sm)
        if k < 0:
            for i in range(len(code)):
                sm = 0
                for j in range(len(code)+k+i,len(code)+i):
                    circular_index =  j % len(code) 
                    sm += code[circular_index]
                decode.append(sm)
                    
        return decode
                    
                    
                    
                    
                    
                    
s = Solution()
print(s.decrypt([2,4,9,3],-2))



# class Solution(object):
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