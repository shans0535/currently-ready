# class Node:
#     def __init__(self, value):
#         self.value = value
#         self.next = None


# class LinkedList:
#     def __init__(self, value):
#         new_node = Node(value)
#         self.head = new_node
#         self.tail = new_node
#         self.length = 1

#     def print_list(self):
#         temp = self.head
#         while temp is not None:
#             print(temp.value)
#             temp = temp.next

#     def append(self, value):
#         new_node = Node(value)
#         if self.length == 0:
#             self.head = new_node
#             self.tail = new_node
#         else:
#             self.tail.next = new_node
#             self.tail = new_node
#         self.length += 1
#         return True

#     def pop(self):
#         if self.length == 0:
#             return None
#         temp = self.head
#         pre = self.head
#         while (temp.next):
#             pre = temp
#             temp = temp.next
#         self.tail = pre
#         self.tail.next = None
#         self.length -= 1
#         if self.length == 0:
#             self.head = None
#             self.tail = None
#         return temp

#     def prepend(self, value):
#         new_node = Node(value)
#         if self.length == 0:
#             self.head = new_node
#             self.tail = new_node
#         else:
#             new_node.next = self.head
#             self.head = new_node
#         self.length += 1
#         return True

#     def pop_first(self):
#         if self.length == 0:
#             return None
#         temp = self.head
#         self.head = self.head.next
#         temp.next = None
#         self.length -= 1
#         if self.length == 0:
#             self.tail = None
#         return temp

#     def get(self, index):
#         if index < 0 or index >= self.length:
#             return None
#         temp = self.head
#         for _ in range(index):
#             temp = temp.next
#         return temp

#     def set_value(self, index, value):
#         temp = self.get(index)
#         if temp:
#             temp.value = value
#             return True
#         return False

#     def insert(self, index, value):
#         if index < 0 or index > self.length:
#             return False
#         if index == 0:
#             return self.prepend(value)
#         if index == self.length:
#             return self.append(value)
#         new_node = Node(value)
#         temp = self.get(index - 1)
#         new_node.next = temp.next
#         temp.next = new_node
#         self.length += 1
#         return True

#     def remove(self, index):
#         if index < 0 or index >= self.length:
#             return None
#         if index == 0:
#             return self.pop_first()
#         if index == self.length - 1:
#             return self.pop()
#         pre = self.get(index - 1)
#         temp = pre.next
#         pre.next = temp.next
#         temp.next = None
#         self.length -= 1
#         return temp

#     def reverse(self):
#         temp = self.head
#         self.head = self.tail
#         self.tail = temp
#         after = temp.next
#         before = None
#         for _ in range(self.length):
#             after = temp.next
#             temp.next = before
#             before = temp
#             temp = after


def loop_detector(head):
    slow = head
    fast = head
    print('finding loop')
    print(f'|slow : {slow.value} , fast : {fast.value}|', end=' ')
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        print(f'|slow : {slow.value} , fast : {fast.value}|', end=' ')
        if slow == fast:
            print('\nloop detected')
            break
    else:
        print('No loops found')
        return
    print(f'Before, slow : {slow.value}, fast : {fast.value}')
    slow = head
    print('finding meeting point :')
    ptr = fast
    while slow != fast:
        print(f'{slow.value}, {fast.value}', end=' ')
        ptr = fast
        slow = slow.next
        fast = fast.next
    print(f'\nAfter, slow : {slow.value}, fast : {fast.value}')
    return ptr, fast


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        self.head = self.tail = Node(value)
        self.length = 1

    def print_list(self):
        temp = self.head
        while temp:
            print(temp.value)
            temp = temp.next

    def append(self, value):
        if self.length == 0:
            self.tail = self.head = Node(value)
            self.length = 1
            return True
        node = Node(value)
        self.tail.next = node
        self.tail = node
        self.length += 1
        return True

    def prepend(self, value):
        if self.length == 0:
            self.head = self.tail = Node(value)
            self.length = 1
            return True
        node = Node(value)
        node.next = self.head
        self.head = node
        self.length += 1
        return True

    def pop(self):
        if self.length == 0:
            return None
        temp = self.head
        while temp.next is not None:
            prev = temp
            temp = temp.next
        self.tail = prev
        prev.next = None
        self.length -= 1
        if self.length == 0:
            self.head = self.tail = None
        return temp

    def pop_first(self):
        if self.length == 0:
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length -= 1
        if self.length == 0:
            self.head = self.tail = None
        return temp

    def get(self, index):
        if index < 0 and index >= self.length:
            return None
        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp

    def set_value(self, index, value):
        temp = self.get(index)
        if temp:
            temp.value = value

    def reverse(self):
        temp = self.head
        self.head = self.tail
        self.tail = temp
        prev = None
        after = temp.next
        for _ in range(self.length):
            after = temp.next
            temp.next = prev
            prev = temp
            temp = after

    def find_middle_node(self):
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        print(slow.value)
        return slow

    def check_if_loop_exists(self):
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                print('loop exist')
                return slow, fast
        else:
            print('no looop')
            return None

    def break_the_loop(self):
        value = self.check_if_loop_exists()
        if value is None:
            print('noo looop')
            return
        slow, fast = value


def test_ll():
    ll = LinkedList(0)
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.prepend(-1)
    ll.prepend(-2)
    ll.prepend(-3)
    ll.prepend(-4)
    ll.print_list()
    temp = ll.pop()
    print(f'value removed {temp.value}')
    ll.print_list()
    temp = ll.pop_first()
    print(f'value removed {temp.value}')
    ll.print_list()
    print('value at index 3', ll.get(5))
    # ll.set_value(3, 10)
    # ll.print_list()
    # ll.insert(3, 100)
    # ll.print_list()
    # print(ll.get(3).value)
    ll.reverse()
    print('after reverse')
    ll.print_list()
    ll.reverse()
    print('after reverse')
    ll.print_list()
    temp = ll.find_middle_node()
    print('middle node ', temp.value)
    ll.check_if_loop_exists()
    ll.tail.next = temp
    print('connecting tail to head')
    ll.check_if_loop_exists()
    a, b = loop_detector(ll.head)
    print(a.value, b.value)


if __name__ == '__main__':

    test_ll()
