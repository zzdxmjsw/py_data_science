from threading import Thread
from queue import Queue
from time import sleep

q = Queue()
num =2
jobs = 10
def do(num):
    print(num)

def working():
    while True:
        num = q.get()
        do(num)
        sleep(1)
        q.task_done()

for i in range(num):
    t = Thread(target=working)
    t.setDaemon(True)
    t.start()

for j in range(jobs):
    q.put(j)

q.join()


from twisted.web.client import getPage
from twisted.internet import reactor
from twisted.web.client import Agent
link = 'http://www.baidu.com'
def parse(data,url):
    print(len(data),url)

def fetch_error(error,url):
    print(error.getErrorMessage(),url)

getPage(link)