# 645. Set Mismatch

class Solution(object):
    def findErrorNums(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        mn = min(nums)
        mx = max(nums)
        lst = []
        test = list(range(1,len(nums)+1))
        for i in test:
            if nums.count(i) == 2:
                lst.insert(0,i)
            if i not in nums:
                lst.append(i)
            if len(lst) == 2:
                break
        
        return lst

        

        
s = Solution()
print(s.findErrorNums([2,2]))

# class Solution(object):
#     def findErrorNums(self, nums):
#         duplicate = -1
#         missing = -1

#         # Find the duplicate
#         for num in nums:
#             idx = abs(num) - 1
#             if nums[idx] < 0:
#                 duplicate = abs(num)
#             else:
#                 nums[idx] *= -1

#         # Find the missing
#         for i in range(len(nums)):
#             if nums[i] > 0:
#                 missing = i + 1
#                 break

#         return [duplicate, missing]

# class Solution(object):
#     def findErrorNums(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: List[int] [1,2,2,3]
#         """
#         expected_sum = sum(i for i in range(1, len(nums)+1))
#         actual_sum = sum(nums)
#         unique_sum = sum(set(nums))
        

#         return [actual_sum - unique_sum, expected_sum - unique_sum]