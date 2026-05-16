# 4. Median of two sorted arrays
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        # a = []
        # for i in nums1:
        #     a.append(i)
        # for j in nums2:
        #     a.append(j)
        # a.sort()
        # n = len(a)
        # mid = n //2
        # if n%2 == 0:
        #     return (a[mid-1]+a[mid])/2.0
        # else:
        #     return a[mid]
        m = len(nums1)
        n = len(nums2)
        t = m + n 
        h = t //2
        prev, curr = 0,0
        i,j = 0,0
        for k in range(h+1):
            prev = curr
            if i < m and (j <= n or nums1[i] <= nums2[j] ):
                curr = nums1[i]
                i += 1
            else:
                curr = nums2[j]
                j += 1

        if t%2 ==1:
            return curr
        return (curr+prev) /2


        
s = Solution()
print(s.findMedianSortedArrays([1,3],[2,4]))