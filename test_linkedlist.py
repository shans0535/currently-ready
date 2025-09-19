import pytest
from singly_linked_list_leetcode import (
    Node,
    SinglyLinkedList,
    reverseList,
    mergeTwoLists,
    hasCycle,
    getIntersectionNode,
    isPalindrome,
    oddEvenList,
    rotateRight,
    reverseKGroup,
    RandomNode,
    copyRandomList,
    swapPairs,
    reverseBetween,
    partition

)


def list_to_linkedlist(values):
    """Helper: convert Python list to linked list"""
    if not values:
        return None
    head = Node(values[0])
    curr = head
    for v in values[1:]:
        curr.next = Node(v)
        curr = curr.next
    return head


def linkedlist_to_list(head):
    """Helper: convert linked list to Python list"""
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result


# ------------------------------
# Tests for SinglyLinkedList class
# ------------------------------

def test_append_and_display(capsys):
    sll = SinglyLinkedList()
    sll.append(1)
    sll.append(2)
    sll.append(3)
    sll.display()
    captured = capsys.readouterr()
    assert "1 -> 2 -> 3" in captured.out


def test_reverse():
    sll = SinglyLinkedList()
    for v in [1, 2, 3]:
        sll.append(v)
    sll.reverse()
    assert linkedlist_to_list(sll.head) == [3, 2, 1]


def test_is_palindrome_true():
    sll = SinglyLinkedList()
    for v in [1, 2, 3, 2, 1]:
        sll.append(v)
    assert sll.is_palindrome() is True


def test_is_palindrome_false():
    sll = SinglyLinkedList()
    for v in [1, 2, 3]:
        sll.append(v)
    assert sll.is_palindrome() is False


def test_odd_even_list():
    sll = SinglyLinkedList()
    for v in [1, 2, 3, 4, 5]:
        sll.append(v)
    sll.odd_even_list()
    assert linkedlist_to_list(sll.head) == [1, 3, 5, 2, 4]


# ------------------------------
# Tests for LeetCode Functions
# ------------------------------

def test_reverseList():
    head = list_to_linkedlist([1, 2, 3])
    new_head = reverseList(head)
    assert linkedlist_to_list(new_head) == [3, 2, 1]


def test_mergeTwoLists():
    l1 = list_to_linkedlist([1, 2, 4])
    l2 = list_to_linkedlist([1, 3, 4])
    merged = mergeTwoLists(l1, l2)
    assert linkedlist_to_list(merged) == [1, 1, 2, 3, 4, 4]


def test_hasCycle_true():
    head = list_to_linkedlist([1, 2, 3])
    head.next.next.next = head.next  # create cycle
    assert hasCycle(head) is True


def test_hasCycle_false():
    head = list_to_linkedlist([1, 2, 3])
    assert hasCycle(head) is False


def test_getIntersectionNode():
    common = list_to_linkedlist([8, 10])
    headA = list_to_linkedlist([3, 7])
    headB = list_to_linkedlist([99])
    # Attach intersection
    headA.next.next = common
    headB.next = common
    assert getIntersectionNode(headA, headB) == common


def test_isPalindrome_true():
    head = list_to_linkedlist([1, 2, 2, 1])
    assert isPalindrome(head) is True


def test_isPalindrome_false():
    head = list_to_linkedlist([1, 2])
    assert isPalindrome(head) is False


def test_oddEvenList():
    head = list_to_linkedlist([2, 1, 3, 5, 6, 4, 7])
    new_head = oddEvenList(head)
    assert linkedlist_to_list(new_head) == [2, 3, 6, 7, 1, 5, 4]


def test_rotateRight():
    head = list_to_linkedlist([1, 2, 3, 4, 5])
    rotated = rotateRight(head, 2)
    assert linkedlist_to_list(rotated) == [4, 5, 1, 2, 3]


def test_reverseKGroup():
    head = list_to_linkedlist([1, 2, 3, 4, 5])
    new_head = reverseKGroup(head, 2)
    assert linkedlist_to_list(new_head) == [2, 1, 4, 3, 5]


def test_copyRandomList():
    a = RandomNode(1)
    b = RandomNode(2)
    a.next = b
    a.random = b
    b.random = a
    copied = copyRandomList(a)
    assert copied.val == 1
    assert copied.random.val == 2
    assert copied.next.val == 2
    assert copied.next.random.val == 1


def list_to_linkedlist(values):
    """Helper: convert Python list to linked list"""
    if not values:
        return None
    head = Node(values[0])
    curr = head
    for v in values[1:]:
        curr.next = Node(v)
        curr = curr.next
    return head


def linkedlist_to_list(head):
    """Helper: convert linked list to Python list"""
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result


# ------------------------------
# Regular Tests
# ------------------------------

def test_append_and_display(capsys):
    sll = SinglyLinkedList()
    sll.append(1)
    sll.append(2)
    sll.append(3)
    sll.display()
    captured = capsys.readouterr()
    assert "1 -> 2 -> 3" in captured.out


def test_reverse():
    sll = SinglyLinkedList()
    for v in [1, 2, 3]:
        sll.append(v)
    sll.reverse()
    assert linkedlist_to_list(sll.head) == [3, 2, 1]


def test_is_palindrome_true():
    sll = SinglyLinkedList()
    for v in [1, 2, 3, 2, 1]:
        sll.append(v)
    assert sll.is_palindrome() is True


def test_is_palindrome_false():
    sll = SinglyLinkedList()
    for v in [1, 2, 3]:
        sll.append(v)
    assert sll.is_palindrome() is False


def test_odd_even_list():
    sll = SinglyLinkedList()
    for v in [1, 2, 3, 4, 5]:
        sll.append(v)
    sll.odd_even_list()
    assert linkedlist_to_list(sll.head) == [1, 3, 5, 2, 4]


def test_reverseList():
    head = list_to_linkedlist([1, 2, 3])
    new_head = reverseList(head)
    assert linkedlist_to_list(new_head) == [3, 2, 1]


def test_mergeTwoLists():
    l1 = list_to_linkedlist([1, 2, 4])
    l2 = list_to_linkedlist([1, 3, 4])
    merged = mergeTwoLists(l1, l2)
    assert linkedlist_to_list(merged) == [1, 1, 2, 3, 4, 4]


def test_hasCycle_true():
    head = list_to_linkedlist([1, 2, 3])
    head.next.next.next = head.next  # create cycle
    assert hasCycle(head) is True


def test_hasCycle_false():
    head = list_to_linkedlist([1, 2, 3])
    assert hasCycle(head) is False


def test_getIntersectionNode():
    common = list_to_linkedlist([8, 10])
    headA = list_to_linkedlist([3, 7])
    headB = list_to_linkedlist([99])
    headA.next.next = common
    headB.next = common
    assert getIntersectionNode(headA, headB) == common


def test_isPalindrome_true():
    head = list_to_linkedlist([1, 2, 2, 1])
    assert isPalindrome(head) is True


def test_isPalindrome_false():
    head = list_to_linkedlist([1, 2])
    assert isPalindrome(head) is False


def test_oddEvenList():
    head = list_to_linkedlist([2, 1, 3, 5, 6, 4, 7])
    new_head = oddEvenList(head)
    assert linkedlist_to_list(new_head) == [2, 3, 6, 7, 1, 5, 4]


def test_rotateRight():
    head = list_to_linkedlist([1, 2, 3, 4, 5])
    rotated = rotateRight(head, 2)
    assert linkedlist_to_list(rotated) == [4, 5, 1, 2, 3]


def test_reverseKGroup():
    head = list_to_linkedlist([1, 2, 3, 4, 5])
    new_head = reverseKGroup(head, 2)
    assert linkedlist_to_list(new_head) == [2, 1, 4, 3, 5]


def test_copyRandomList():
    a = RandomNode(1)
    b = RandomNode(2)
    a.next = b
    a.random = b
    b.random = a
    copied = copyRandomList(a)
    assert copied.val == 1
    assert copied.random.val == 2
    assert copied.next.val == 2
    assert copied.next.random.val == 1


# ------------------------------
# Edge Case Tests
# ------------------------------

def test_empty_list_reverseList():
    assert reverseList(None) is None


def test_empty_list_isPalindrome():
    assert isPalindrome(None) is True


def test_single_node_reverseList():
    head = list_to_linkedlist([42])
    new_head = reverseList(head)
    assert linkedlist_to_list(new_head) == [42]


def test_single_node_isPalindrome():
    head = list_to_linkedlist([7])
    assert isPalindrome(head) is True


def test_rotateRight_single_node():
    head = list_to_linkedlist([99])
    rotated = rotateRight(head, 3)
    assert linkedlist_to_list(rotated) == [99]


def test_large_list_reverse():
    n = 10000
    head = list_to_linkedlist(list(range(1, n + 1)))
    new_head = reverseList(head)
    result = linkedlist_to_list(new_head)
    assert result == list(range(n, 0, -1))


def test_find_kth_from_end():
    sll = SinglyLinkedList()
    for val in [1, 2, 3, 4, 5]:
        sll.append(val)
    # 2nd from end should be 4
    kth_node = sll.find_kth_from_end(2)
    assert kth_node.data == 4
    # 5th from end should be 1
    kth_node = sll.find_kth_from_end(5)
    assert kth_node.data == 1
    # k > length
    assert sll.find_kth_from_end(6) is None


def test_remove_duplicates():
    sll = SinglyLinkedList()
    for val in [1, 3, 2, 3, 4, 1, 5]:
        sll.append(val)
    sll.remove_duplicates()
    assert linkedlist_to_list(sll.head) == [1, 3, 2, 4, 5]


def test_binary_to_decimal():
    sll = SinglyLinkedList()
    for bit in [1, 0, 1, 1]:  # binary 1011 = 11
        sll.append(bit)
    assert sll.binary_to_decimal() == 11
    # Single bit
    sll2 = SinglyLinkedList()
    sll2.append(1)
    assert sll2.binary_to_decimal() == 1


def test_partition():
    head = list_to_linkedlist([1, 4, 3, 2, 5, 2])
    new_head = partition(head, 3)
    # All nodes < 3 come first: 1,2,2, then nodes >=3:4,3,5
    result = linkedlist_to_list(new_head)
    assert result[:3] == [1, 2, 2]
    assert all(x >= 3 for x in result[3:])


def test_reverseBetween():
    head = list_to_linkedlist([1, 2, 3, 4, 5])
    new_head = reverseBetween(head, 2, 4)
    assert linkedlist_to_list(new_head) == [1, 4, 3, 2, 5]
    # reverse single element: should remain unchanged
    head2 = list_to_linkedlist([1, 2, 3])
    new_head2 = reverseBetween(head2, 2, 2)
    assert linkedlist_to_list(new_head2) == [1, 2, 3]


def test_swapPairs():
    head = list_to_linkedlist([1, 2, 3, 4])
    new_head = swapPairs(head)
    assert linkedlist_to_list(new_head) == [2, 1, 4, 3]
    # odd number of nodes
    head2 = list_to_linkedlist([1, 2, 3])
    new_head2 = swapPairs(head2)
    assert linkedlist_to_list(new_head2) == [2, 1, 3]
    # single node
    head3 = list_to_linkedlist([1])
    new_head3 = swapPairs(head3)
    assert linkedlist_to_list(new_head3) == [1]
    # empty list
    assert swapPairs(None) is None
