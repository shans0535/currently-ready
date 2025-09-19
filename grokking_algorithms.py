# quick sort
from random import randint


def qsort(array):
    if len(array) < 2:
        return array
    less = []
    greater = []
    pivot = array[0]
    for i in array[1:]:
        if i < pivot:
            less.append(i)
        else:
            greater.append(i)
    return qsort(less)+[pivot]+qsort(greater)


def bbsort(nums):
    n = len(nums)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
                swapped = True
        if swapped is False:
            break
    return nums


def bsearch(nums, target, asc=True):
    high = len(nums)+1
    low = 0
    while low <= high:
        mid = (low+high)//2
        guess = nums[mid]
        if target == guess:
            return mid
        elif target < guess:
            high = mid-1
        else:
            low = mid+1
    return None


if __name__ == '__main__':
    l1 = [randint(1, 50) for i in range(50)]
    l1 = qsort(l1)
    print(l1)
    l2 = bbsort(l1)

    print(bsearch(l1, 10))
    print(l2)
