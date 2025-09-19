# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Singly Linked List class
class SinglyLinkedList:
    def __init__(self):
        self.head = None
    # Insert at the end

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    # Insert at the beginning
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    # Delete a node by value
    def delete(self, key):
        temp = self.head
        if temp and temp.data == key:
            self.head = temp.next
            temp = None
            return

        prev = None
        while temp and temp.data != key:
            prev = temp
            temp = temp.next

        if not temp:
            return

        prev.next = temp.next
        temp = None

    # ----------------------
    # Pop first element
    # ----------------------
    def pop_first(self):
        """Remove and return the first node's value. Returns None if empty."""
        if not self.head:
            return None
        val = self.head.data
        self.head = self.head.next
        return val

    # pop method
    def pop(self):
        """Remove and return the last node's value. Returns None if empty."""
        if not self.head:
            return None
        if not self.head.next:
            val = self.head.data
            self.head = None
            return val
        curr = self.head
        while curr.next.next:
            curr = curr.next
        val = curr.next.data
        curr.next = None
        return val

    # Search for a value
    def search(self, key):
        temp = self.head
        position = 0
        while temp:
            if temp.data == key:
                return f"Found {key} at position {position}"
            temp = temp.next
            position += 1
        return f"{key} not found in the list"

    # Iterative reverse
    def reverse(self):
        prev = None
        current = self.head
        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt
        self.head = prev

    # Recursive reverse helper
    def _reverse_recursive(self, current, prev):
        if not current:
            return prev
        nxt = current.next
        current.next = prev
        return self._reverse_recursive(nxt, current)

    # Public method for recursive reverse
    def reverse_recursive(self):
        self.head = self._reverse_recursive(self.head, None)

    # Find the middle element (slow & fast pointer)
    def find_middle(self):
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow.data if slow else None

    # Detect cycle using Floyd's cycle-finding algorithm
    def has_cycle(self):
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    # Remove cycle if it exists
    def remove_cycle(self):
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return  # No cycle

        slow = self.head
        while slow != fast:
            slow = slow.next
            fast = fast.next

        while fast.next != slow:
            fast = fast.next

        fast.next = None

    # Merge two sorted linked lists
    def _merge_sorted(self, left, right):
        if not left:
            return right
        if not right:
            return left

        if left.data <= right.data:
            result = left
            result.next = self._merge_sorted(left.next, right)
        else:
            result = right
            result.next = self._merge_sorted(left, right.next)
        return result

    # Split the list into two halves
    def _split(self, head):
        if not head or not head.next:
            return head, None

        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        middle = slow.next
        slow.next = None
        return head, middle

    # Recursive merge sort
    def _merge_sort(self, head):
        if not head or not head.next:
            return head

        left, right = self._split(head)
        left = self._merge_sort(left)
        right = self._merge_sort(right)

        return self._merge_sorted(left, right)

    # Public sort method
    def sort(self):
        self.head = self._merge_sort(self.head)

    # Remove duplicates in a sorted list
    def remove_duplicates_sorted(self):
        current = self.head
        while current and current.next:
            if current.data == current.next.data:
                current.next = current.next.next
            else:
                current = current.next

    # Remove duplicates in an unsorted list (using set)
    def remove_duplicates_unsorted(self):
        seen = set()
        current = self.head
        prev = None
        while current:
            if current.data in seen:
                prev.next = current.next
            else:
                seen.add(current.data)
                prev = current
            current = current.next

    # Detect intersection of two linked lists
    @staticmethod
    def get_intersection(list1, list2):
        if not list1.head or not list2.head:
            return None

        p1 = list1.head
        p2 = list2.head

        while p1 != p2:
            p1 = p1.next if p1 else list2.head
            p2 = p2.next if p2 else list1.head

        return p1.data if p1 else None

    # Check if two linked lists are identical
    @staticmethod
    def are_identical(list1, list2):
        p1 = list1.head
        p2 = list2.head

        while p1 and p2:
            if p1.data != p2.data:
                return False
            p1 = p1.next
            p2 = p2.next

        return p1 is None and p2 is None

    # Check if the list is a palindrome
    def is_palindrome(self):
        if not self.head or not self.head.next:
            return True  # Empty or single node is always palindrome

        # Step 1: Find middle
        slow, fast = self.head, self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse second half
        prev = None
        curr = slow
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        second_half = prev

        # Step 3: Compare first and second half
        first, second = self.head, second_half
        palindrome = True
        while second:  # Only need to check second half
            if first.data != second.data:
                palindrome = False
                break
            first = first.next
            second = second.next

        # Step 4: Restore (optional)
        prev = None
        curr = second_half
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        return palindrome

    # Display all nodes
    def display(self):
        nodes = []
        temp = self.head
        while temp:
            nodes.append(str(temp.data))
            temp = temp.next
        print(" -> ".join(nodes) if nodes else "List is empty")

    def find_kth_from_end(self, k):
        """Return k-th node from the end (1-based)."""
        slow = fast = self.head
        for _ in range(k):
            if not fast:
                return None
            fast = fast.next
        while fast:
            slow = slow.next
            fast = fast.next
        return slow

    def remove_duplicates(self):
        """Remove duplicates from an unsorted linked list."""
        seen = set()
        curr = self.head
        prev = None
        while curr:
            if curr.data in seen:
                prev.next = curr.next
            else:
                seen.add(curr.data)
                prev = curr
            curr = curr.next

    def binary_to_decimal(self):
        """Convert binary number (linked list bits) to decimal."""
        curr = self.head
        num = 0
        while curr:
            num = (num << 1) | curr.data
            curr = curr.next
        return num

    def odd_even_list(self):
        """Rearrange nodes into odd-even order (LeetCode #328).
        Time: O(n), Space: O(1)"""
        if not self.head or not self.head.next:
            return
        odd, even, even_head = self.head, self.head.next, self.head.next
        while even and even.next:
            odd.next = even.next
            odd = odd.next
            even.next = odd.next
            even = even.next
        odd.next = even_head

# ==============================
# Singly Linked List + LeetCode
# With Time & Space Complexity
# ==============================


# For LeetCode #138 (Random Pointer List)
class RandomNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


# ==============================
# LeetCode-Style Solutions
# ==============================

def reverseList(head):  # #206
    """Reverse linked list.
    Time: O(n), Space: O(1)"""
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def mergeTwoLists(l1, l2):  # #21
    """Merge two sorted linked lists.
    Time: O(m+n), Space: O(1)"""
    dummy = Node(0)
    tail = dummy
    while l1 and l2:
        if l1.data < l2.data:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next


def hasCycle(head):  # #141
    """Detect cycle in a linked list (Floyd’s algorithm).
    Time: O(n), Space: O(1)"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


def getIntersectionNode(headA, headB):  # #160
    """Find intersection of two linked lists.
    Time: O(m+n), Space: O(1)"""
    if not headA or not headB:
        return None
    p1, p2 = headA, headB
    while p1 != p2:
        p1 = p1.next if p1 else headB
        p2 = p2.next if p2 else headA
    return p1


def isPalindrome(head):  # #234
    """Check if linked list is palindrome.
    Time: O(n), Space: O(1)"""
    if not head or not head.next:
        return True
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    prev, curr = None, slow
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    first, second = head, prev
    while second:
        if first.data != second.data:
            return False
        first, second = first.next, second.next
    return True


def oddEvenList(head):  # #328
    """Rearrange odd/even nodes.
    Time: O(n), Space: O(1)"""
    if not head or not head.next:
        return head
    odd, even, even_head = head, head.next, head.next
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head


# ------------------------------
# Hard Problems
# ------------------------------

def rotateRight(head, k):  # #61
    """Rotate list right by k places.
    Time: O(n), Space: O(1)"""
    if not head or not head.next:
        return head
    length, tail = 1, head
    while tail.next:
        tail = tail.next
        length += 1
    tail.next = head
    k = k % length
    steps_to_new_head = length - k
    new_tail = head
    for _ in range(steps_to_new_head - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head


def reverseKGroup(head, k):  # #25
    """Reverse nodes in groups of k.
    Time: O(n), Space: O(1)"""

    def get_kth(curr, k):
        while curr and k > 0:
            curr = curr.next
            k -= 1
        return curr

    dummy = Node(0)
    dummy.next = head
    group_prev = dummy

    while True:
        kth = get_kth(group_prev, k)
        if not kth:
            break
        group_next = kth.next

        prev, curr = kth.next, group_prev.next
        while curr != group_next:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp

        tmp = group_prev.next
        group_prev.next = kth
        group_prev = tmp

    return dummy.next


def copyRandomList(head):  # #138
    """Copy list with random pointer.
    Time: O(n), Space: O(1) extra"""
    if not head:
        return None
    curr = head
    while curr:
        new_node = RandomNode(curr.val, curr.next, None)
        curr.next = new_node
        curr = new_node.next
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next
    curr = head
    new_head = head.next
    while curr:
        copy = curr.next
        curr.next = copy.next
        if copy.next:
            copy.next = copy.next.next
        curr = curr.next
    return new_head


# ----------------------
# LeetCode-style functions
# ----------------------

def partition(head, x):
    """Partition List (LeetCode 86)."""
    before_head = before = Node(0)
    after_head = after = Node(0)
    while head:
        if head.data < x:
            before.next = head
            before = before.next
        else:
            after.next = head
            after = after.next
        head = head.next
    after.next = None
    before.next = after_head.next
    return before_head.next


def reverseBetween(head, left, right):
    """Reverse Linked List between left and right (LeetCode 92)."""
    if not head or left == right:
        return head

    dummy = Node(0)
    dummy.next = head
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next

    curr = prev.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next


def swapPairs(head):
    """Swap nodes in pairs (LeetCode 24)."""
    dummy = Node(0)
    dummy.next = head
    prev = dummy

    while prev.next and prev.next.next:
        a = prev.next
        b = a.next

        # swap
        prev.next, a.next, b.next = b, b.next, a

        prev = a
    return dummy.next


# ==============================
# Example Usage
# ==============================
if __name__ == "__main__":
    print("=== Rotate List ===")
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)
    rotated = rotateRight(head, 2)
    temp = rotated
    while temp:
        print(temp.data, end=" -> ")
        temp = temp.next
    print("None")

    print("\n=== Reverse K Group ===")
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)
    new_head = reverseKGroup(head, 2)
    temp = new_head
    while temp:
        print(temp.data, end=" -> ")
        temp = temp.next
    print("None")

    print("\n=== Copy List with Random Pointer ===")
    a = RandomNode(1)
    b = RandomNode(2)
    a.next = b
    a.random = b
    b.random = b
    copied = copyRandomList(a)
    print("Original:", a.val, "-> Random:", a.random.val)
    print("Copied:", copied.val, "-> Random:", copied.random.val)
