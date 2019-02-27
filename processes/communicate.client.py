import time
from multiprocessing.managers import BaseManager
from communicate_cfg import task_addr, task_port, task_auth

class Queuemanager(BaseManager):
    pass

Queuemanager.register('get_task_queue')
Queuemanager.register('get_requst_queue')
print('connect to server %s:%s...' % (task_addr, task_port))
manager = Queuemanager(address=(task_addr, task_port), authkey=task_auth.encode('utf-8'))
manager.connect()


task = manager.get_task_queue()
result = manager.get_requst_queue()

while(not task.empty()):
    url = task.get(True, timeout=5)
    print('get %s from task ...' % url)
    time.sleep(1)
    result.put('%s ---- success' % url)

print('worker done')
