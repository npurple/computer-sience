import random
import time, threading

total = 0

class MyThread(threading.Thread):
    def __init__(self, name, urls):
        threading.Thread.__init__(self,name=name)
        self.url_list = urls

    def run(self):
        global total
        print("current %s is running" % threading.current_thread().name)
        for url in self.url_list:
            total += 1
            print("%s ------ %s" % (threading.current_thread().name, url))
            s = random.random()
            print("%s sleep %s" % (threading.current_thread().name, s))
            time.sleep(s)
        print("%s ended" % threading.current_thread().name)

def go(urls):
    global total
    print("current %s is running" % threading.current_thread().name)
    for url in urls:
        total += 1
        print("%s ------ %s" % (threading.current_thread().name, url))
        s = random.random()
        print("%s sleep %s" % (threading.current_thread().name, s))
        time.sleep(s)
    print("%s ended" % threading.current_thread().name)

print("%s is running" % threading.current_thread().name)

t1 = threading.Thread(target=go, name='t1', args = (['url_%s' % i for i in range(2)], ))
t2 = threading.Thread(target=go, name='t2', args = (['url_%s' % i for i in range(2,4)], ))
t3 = MyThread(name='t3', urls=['url_%s' % i for i in range(4,6)])
t4 = MyThread(name='t4', urls=['url_%s' % i for i in range(6,8)])

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print(total)
