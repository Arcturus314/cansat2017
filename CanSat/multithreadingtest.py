import threading

class myThread(threading.Thread):
	def _init_(slef, threadID, name):
		self.threadID = threadID
		self.name = name
	def run(self):
		
def data():

thread1 = myThread(1, "Thread-1", 1)

thread1.start
