import time
import datetime
import threading


class TestThreading(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            # More statements comes here
            print(datetime.datetime.now().__str__() + ' : Start task in the background')

            time.sleep(self.interval)

tr = TestThreading()
time.sleep(1)
print(datetime.datetime.now().__str__() + ' : First output')
time.sleep(2)
print(datetime.datetime.now().__str__() + ' : Second output') 
