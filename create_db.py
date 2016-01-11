from app import redis

if __name__ == '__main__':
    accounts_file = file('accounts.txt', 'r')
    for line in accounts_file.readlines():
        print line

    print redis
