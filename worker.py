import redis
from rq import Worker, Queue

conn = redis.from_url('redis://localhost:6379')

if __name__ == '__main__':
    worker = Worker(['default'], connection=conn)
    worker.work()