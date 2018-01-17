import collections, math

Statistics = collections.namedtuple('Statistics', 'mean mode median std_dev')

def read_data(filename, numbers, frequencies):
    for lino, line in enumerate(open(filename, encoding='ascii'), start=1):
        for x in line.split():
            try:
                number = float(x)
                numbers.append(number)
                frequencies[number] += 1
            except ValueError as err:
                print('{0}:{1}: skipping {2}: {3}',format(filename, lino, x, err))


def calculate_statistics(numbers, frequencies):
    mean = sum(numbers) / len(numbers)
    mode = calculate_mode(frequencies, 3)
    median = calculate_median(numbers)
    std_dev = calculate_std_dev(numbers, mean)
    return Statistics(mean, mode, median, std_dev)


def calculate_mode(frequencies, maximum_modes):
    mode = [freq for num, freq in frequencies.items()]
    mode = sorted(mode, reverse=True)
    return mode[:maximum_modes]


def calculate_median(numbers):
    if len(numbers) == 0:
        return None
    numbers = sorted(numbers)
    middle = len(numbers) // 2
    median = numbers[middle]
    if len(numbers) % 2 == 0:
        median = (median + numbers[median + 1]) /2
    return median


def calculate_std_dev(numbers, mean):
    total = 0
    for number in numbers:
        total += ((number - mean) ** 2)
    variance = total / (len(numbers) - 1)
    return math.sqrt(variance)


def print_results(count, statistics):
    real = '9.2f'
    if statistics.mode is None:
        modeline = ''
    elif len(statistics.mode) == 1:
        modeline = 'mode = {0:{fmt}}\n'.format(statistics.mode[0], fmt=real)
    else:
        modeline = ('mode = [' + ', '.join(['{0:.2f}'.format(m) for m in statistics.mode]) + ']\n')
    print('''\
    count = {0:6}
    mean = {1.mean:{fmt}}
    median = {1.median:{fmt}}
    {2}\
    std. dev. = {1.std_dev:{fmt}}'''.format(count, statistics, modeline, fmt=real))


def test():
    testmode1 ={'fwefewf':4, 'wefwef': 0, 'afef': 4,'fas':55}
    testmode2 = {}
    assert calculate_mode(testmode1, 3) == [55, 4, 4]
    assert calculate_mode(testmode2, 3) == []
    testmedian1 = [1,2,3,4,5]
    assert calculate_median(testmedian1) == 3
    testmedian2 = []
    assert calculate_median(testmedian2) == None

if __name__ == '__main__':
    test()
    frequencies = collections.defaultdict(int)
    numbers = []
    read_data(r'.\data\statistics.dat', numbers, frequencies)
    if numbers:
        statistics = calculate_statistics(numbers, frequencies)
        print_results(len(numbers),statistics)
    else:
        print('no numbers found')