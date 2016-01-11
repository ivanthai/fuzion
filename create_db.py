from app import redis
from os import path

if __name__ == '__main__':
    accounts_dir = path.join(
        path.dirname(path.realpath(__file__)), 'accounts.txt'
    )
    with file(accounts_dir, 'r') as accounts_file:
        for line in accounts_file.readlines():
            print line
            id, v_id, a_id = line.split(',')
            redis.rpush('listings', 'listings:'+id)
            redis.hset('listings:'+id, 'airbnb', a_id)
            redis.hset('listings:'+id, 'vrbo', v_id)
