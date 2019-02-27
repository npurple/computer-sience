import time
import queue
from multiprocessing.managers import BaseManager
from communicate_cfg import task_addr, task_port, task_auth

taskq = queue.Queue()
resultq = queue.Queue()

class Queuemanager(BaseManager):
    pass

Queuemanager.register('get_task_queue', callable=lambda:taskq)
Queuemanager.register('get_requst_queue', callable=lambda:resultq)
manager = Queuemanager(address=(task_addr, task_port), authkey=task_auth.encode('utf-8'))

manager.start()

task = manager.get_task_queue()
result = manager.get_requst_queue()

for url in ['url_%s' % i for i in range(10)]:
    print('put task %s ...' % url)
    task.put(url)


print('waiting for get result ...')
for i in range(10):
    print('result is %s' % result.get(timeout=10))

# manager.join()
