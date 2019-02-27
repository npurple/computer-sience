import os


pid = os.fork()
if pid == 0:
    print('im the child(%s) process, my father is %s' % (os.getpid(), os.getppid()))
else:
    print('im the parent(%s) process, my child is %s' % (os.getpid(), pid))
