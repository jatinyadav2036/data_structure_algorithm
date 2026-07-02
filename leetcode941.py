# 941. Valid Mountain Array

class Solution(object):
    def validMountainArray(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """
        if len(arr) < 3:
            return False

        if any(arr[i] == arr[i + 1] for i in range(len(arr) - 1)):
            return False
        mx = arr.index(max(arr))
        if mx == 0 or mx == len(arr)-1:
            return False
        arr1 = arr[:mx]
        arr2 = arr[mx+1:]
        def inc(lst):
            return all(lst[i] < lst[i+1] for i in range(len(lst)-1))

        def dec(lst):
            return all(lst[i] > lst[i+1] for i in range(len(lst)-1))

        return inc(arr1) and dec(arr2)
                    
    # class Solution(object):
    # def validMountainArray(self, arr):
    #     """
    #     :type arr: List[int]
    #     :rtype: bool
    #     """
    #     if len(arr)<3:
    #         return False
    #     i=0
    #     while(i<len(arr)-1 and arr[i]<arr[i+1]):
    #         i+=1
    #     if i==0 or i==len(arr)-1:
    #         return False
        
    #     while(i<len(arr)-1 and arr[i]>arr[i+1]):
    #         i+=1
    #     return i==len(arr)-1