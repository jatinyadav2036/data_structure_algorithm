class Solution(object):
#     def middleNode(self, head):
#         """
#         :type head: Optional[ListNode]
#         :rtype: Optional[ListNode]
#         """
#         if not head:
#             return -1
#         fast=head
#         slow=head
#         while (fast and fast.next):
#             fast=fast.next.next
#             slow=slow.next
#         return slow