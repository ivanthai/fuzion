from app import redis

if __name__ == '__main__':
    with file('accounts.txt', 'r') as accounts_file:
        for line in accounts_file.readlines():
            id, v_id, a_id = line.split(',')
            redis.rpush('listings', 'listings:'+id)
            redis.hset('listings:'+id, 'airbnb', a_id)
            redis.hset('listings:'+id, 'vrbo', v_id)
