# 3541. Find Most Frequent Vowel and Consonant
class Solution(object):
    def maxFreqSum(self, s):
        """
        :type s: str
        :rtype: int
        """
        vowels = ['a', 'e' , 'i' , 'o' , 'u']
        fv = {"a":0}
        fc = {"b":0}
        for i in s :
            if i in vowels:
                fv[i] = fv.get(i,0) + 1
            else:
                fc[i] = fc.get(i,0) + 1
        mxv = max(fv.values()) 
        mxc = max(fc.values())
        return mxv + mxc

        

# class Solution(object):
#     def maxFreqSum(self, s):
#         mp={}
#         for i in s:
#             if i in mp:
#                 mp[i]+=1
#             else: mp[i]=1
#             freq_c=0
            
#             freq_v=0
            
               
#         for key,value in mp.items():
#             if key in "aeiou":
#                 if freq_v<value:
#                     freq_v=value
                    
#             else:
#                 if(freq_c<value):
#                     freq_c=value
#         return (freq_v)+(freq_c)