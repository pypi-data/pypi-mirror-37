# -*- coding=utf-8
from threading import Thread
from logging import getLogger
from six.moves.queue import Queue
from threading import Lock
import threading
import gc
logger = getLogger(__name__)


class WorkerThread(Thread):
    def __init__(self, task_queue, *args, **kwargs):
        super(WorkerThread, self).__init__(*args, **kwargs)

        self._task_queue = task_queue
        self._succ_task_num = 0
        self._fail_task_num = 0
        self._ret = list()

    def run(self):
        while True:
            func, args, kwargs = self._task_queue.get()

            try:
                ret = func(*args, **kwargs)
                self._succ_task_num += 1
                self._ret.append(ret)

            except Exception as e:
                logger.warn(str(e))
                self._fail_task_num += 1
                self._ret.append(e)
            finally:
                self._task_queue.task_done()
            if self._task_queue.empty():
                break

    def get_result(self):
            return self._succ_task_num, self._fail_task_num, self._ret


class SimpleThreadPool:

    def __init__(self, num_threads=5):
        self._num_threads = num_threads
        self._queue = Queue()
        self._lock = Lock()
        self._active = False
        self._workers = list()
        self._finished = False

    def add_task(self, func, *args, **kwargs):
        if not self._active:
            with self._lock:
                if not self._active:
                    self._active = True

                    for i in range(self._num_threads):
                        w = WorkerThread(self._queue)
                        self._workers.append(w)
                        w.start()

        self._queue.put((func, args, kwargs))

    def wait_completion(self):
        self._queue.join()
        self._finished = True

    def get_result(self):
        assert self._finished
        detail = [worker.get_result() for worker in self._workers]
        succ_all = all([tp[1] == 0 for tp in detail])
        return {'success_all': succ_all, 'detail': detail}

def aaa(id,jd):
    lock.acquire()
    try:
        print ("aaa"+str(id)+str(jd))
        time.sleep(0.1)
    finally:
        lock.release()

def bbb(id):
    lock.acquire()
    try:
        print ("bbb"+str(id))
    finally:
        lock.release()

def aab(id):
    pool = SimpleThreadPool(5)
    for i in range(10):
        pool.add_task(aaa,id,i)
    pool.wait_completion()
    bbb(id)

def ccc(i):
    lock.acquire()
    try:
        print ("ccc"+str(i))
    finally:
        lock.release()

if __name__ == '__main__':
    lock = threading.Lock()
    pool2 = SimpleThreadPool(5)
    for i in range(10):
        pool2.add_task(aab,i)
        pool2.add_task(ccc,i)
#     pool2.wait_completion()
