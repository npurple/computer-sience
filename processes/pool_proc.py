from multiprocessing import Pool
import os,time,random

def deal(name):
    print('this is child task name(%s), pid(%s) start running' % (name, os.getpid()))
    # time.sleep(random.random() * 3)
    time.sleep(3)
    print('Task(%s) ending' % name)


print('current process(%s) --- 1 ' % os.getpid())
p = Pool(processes=3)
for i in range(5):
    p.apply_async(deal, args=(i,))

print('before close')
p.close()
'''
print('before join')
p.join()
print('after join')
'''

print('before sleep')
time.sleep(6)
print('after sleep')
print('current process(%s) --- 2 ' % os.getpid())
