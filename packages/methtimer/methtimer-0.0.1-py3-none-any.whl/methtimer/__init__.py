from time import time

def MethTimer(func):
	def fun(*args,**kwargs):
		before = time()
		ret = func(*args,**kwargs)
		after = time()
		print("Elapsed Time:",(after-before) * 1000,"ms")
		return ret
	return fun

