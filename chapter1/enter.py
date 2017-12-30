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

if numbers:
    print('numbers:',numbers)
    print('count =', len(numbers),'sum =', sum, 'lowest =', lowest, 'highest = ', highest, 'mean = ', sum/len(numbers))
else:
    print('You input nothing')