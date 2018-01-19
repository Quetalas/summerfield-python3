"""
Создаёт уникальные имена пользователей на основе уникального id,
Имени, Отчества(может отсутствовать), Фамилии, названия отдела
"""
import collections, sys

ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)

User = collections.namedtuple('User', 'username forename, middlename surname id')

def main():
    if  len(sys.argv) == 1:
        filenames = ['data/users.txt']
    elif sys.argv[1] in {'-h', '--help'}:
        print('usage: {0} file1 [file2 [... fileN]]'.format(sys.argv[0]))
        sys.exit()
    else:
        filenames = sys.argv[1:]
    usernames = set() #для имён пользователей
    users = {} # сами пользователи
    for filename in filenames:
        for line in open(filename, encoding='utf8'):
            line =line.rstrip()
            if line:
                user = process_line(line, usernames)
                users[(user.surname.lower(), user.forename.lower(),user.id)] = user # ключ обеспечивает возможность сортировки
    print_users(users)

def process_line(line, usernames):
    '''
    Создаёт объект пользователя типа User(username=.., forename=..., middlename=...,
    surname=..., id=...)
    :param line:
    :param usernames:
    :return:
    '''
    fields = line.split(':')
    username = generate_username(fields, usernames)
    user = User(username, fields[FORENAME], fields[MIDDLENAME], fields[SURNAME],
                fields[ID])
    return user


def generate_username(fields, usernames):
    username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] + fields[SURNAME]).replace('-','').replace("'", ""))
    username = original_name = username[:8].lower()
    count = 1
    while username in usernames:
        username = '{0}{1}'.format(original_name, count)
        count += 1
    usernames.add(username)
    return username


def print_users(users):
    namewidth = 32
    usernamewidth = 9

    print("{0:<{nw}} {1:^6} {2:{uw}}".format('Name', "ID",
                                             'Username',
                                             nw=namewidth, uw=usernamewidth))
    print("{0:-<{nw}} {0:-<6} {0:-<{uw}}".format('', nw=namewidth, uw=usernamewidth))

    for key in sorted(users):
        user = users[key]
        initial = ''
        if user.middlename:
            initial = " " + user.middlename
        name = '{0.surname}, {0.forename}{1}'.format(user, initial)
        print('{0:.<{nw}} ({1.id:4}) {1.username:{uw}}'.format(
            name, user, nw=namewidth, uw=usernamewidth))

if __name__ == '__main__':
    main()