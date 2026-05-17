# 23. Merge k Sorted Lists

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# class Solution(object):
#     def mergeKLists(self, lists):
#         a = []
#         for i in lists:
#             for j in i:
#                 a.append(j)
#         a.sort()

#         return a
    
# s = Solution()
# print(s.mergeKLists([[1,4,5],[1,3,4],[2,6]]))
        
# class Solution(object):
#     def mergeKLists(self, lists):
#         arr = []

#         # Collect all values
#         for node in lists:
#             while node:
#                 arr.append(node.val)
#                 node = node.next

#         # Sort values
#         arr.sort()

#         # Build result linked list
#         dummy = ListNode(0)
#         curr = dummy

#         for val in arr:
#             curr.next = ListNode(val)
#             curr = curr.next

#         return dummy.next
    
# s = Solution()
# print(s.mergeKLists([[1,4,5],[1,3,4],[2,6]]))
        

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(self, lists):
        arr = []

        for node in lists:
            while node:
                arr.append(node.val)
                node = node.next

        arr.sort()

        dummy = ListNode()
        curr = dummy

        for val in arr:
            curr.next = ListNode(val)
            curr = curr.next

        return dummy.next


def make_linked_list(arr):
    dummy = ListNode()
    curr = dummy

    for x in arr:
        curr.next = ListNode(x)
        curr = curr.next

    return dummy.next


def print_linked_list(head):
    while head:
        print(head.val, end=" -> ")
        head = head.next
    print("None")


lists = [
    make_linked_list([1,4,5]),
    make_linked_list([1,3,4]),
    make_linked_list([2,6])
]

s = Solution()
result = s.mergeKLists(lists)

print_linked_list(result)