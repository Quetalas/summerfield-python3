"""
Просит ввести цифры, а затем выводит их сумму,
максимальное, минимальное , среднее и их количество
"""

msg='enter a number or Enter to finish '
numbers = []
sum = 0
lowest = highest = None
while True:
    i = input(msg)
    if i == '':
        break
    try:
        i = int(i)
        sum += i
        numbers.append(i)
        if not lowest:
            lowest = i
            highest = i
        else:
            if i < lowest:
                lowest = i
            if i > highest:
                highest = i
    except ValueError as err:
        print(err)


def merge(left, right):
    j = 0
    i = 0
    res = []
    while True:
        rnext = lnext = None
        if i < len(right):
            rnext = right[i]
        if j < len(left):
            lnext = left[j]
        if lnext and rnext:
            if lnext <= rnext:
                res.append(lnext)
                j += 1
            else:
                res.append(rnext)
                i += 1
        elif lnext:
            res.append(lnext)
            j += 1
        elif rnext:
            res.append(rnext)
            i += 1
        else:
            break
    print(res)
    return res






def sort(nums):
    import math
    if len(nums) == 1:
        return nums
    else:
        mid = math.ceil(len(nums)/2)
        #отсортированные половины
        left = sort(nums[:mid])
        right = sort(nums[mid:])
        #объединяем их
        return merge(left, right)

if numbers:
    print('numbers:',numbers)
    print('count =', len(numbers),'sum =', sum, 'lowest =', lowest, 'highest = ', highest, 'mean = ', sum/len(numbers))
    print('sorted: ', sort(numbers))
else:
    print('You input nothing')