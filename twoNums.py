# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None
'''
给定两个非空链表来表示两个非负整数。位数按照逆序方式存储，它们的每个节点只存储单个数字。将两数相加返回一个新的链表。

你可以假设除了数字 0 之外，这两个数字都不会以零开头。

示例：

输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
输出：7 -> 0 -> 8
原因：342 + 465 = 807
'''
class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        num1 = []
        num2 = []
        nums1 = ''
        nums2 = ''
        listNodes = []
        num1.append(l1.val)
        num2.append(l2.val)
        while (l1.next):
            l1 = l1.next
            num1.append(l1.val)

        while (l2.next):
            l2 = l2.next
            num2.append(l2.val)
        for n in num1:
            nums1 += str(n)

        for n in num2:
            nums2 += str(n)
        res = int(nums1[::-1]) + int(nums2[::-1])
        for i in reversed(str(res)):
            listNodes.append(ListNode(int(i)))

        for l in range(len(listNodes) - 1):
            listNodes[l].next = listNodes[l + 1]

        return listNodes[0]