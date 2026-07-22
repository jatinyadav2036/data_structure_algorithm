# 3940. Limit Occurrences in Sorted Array

class Solution(object):
    def limitOccurrences(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        if not nums:
            return []
            
        write_index = 1
        cnt = 1
        
        # Loop through the list starting from the second element
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                cnt += 1
            else:
                cnt = 1
                
            # If the count is within limits, keep the element
            if cnt <= k:
                nums[write_index] = nums[i]
                write_index += 1
                
        # Slice the list to remove the leftover items at the end
        return nums[:write_index]

s = Solution()
print(s.limitOccurrences([1, 1, 1, 2, 2, 3], 2))  # Output: [1, 1, 2, 2, 3]
print(s.limitOccurrences([5, 5], 1))              # Output: [5]


# class Solution(object):
#     def limitOccurrences(self, nums, k):
#         ans=[]
#         for i in range(len(nums)):
#             if ans.count(nums[i])<k:
#                 ans.append(nums[i])
#         return ans