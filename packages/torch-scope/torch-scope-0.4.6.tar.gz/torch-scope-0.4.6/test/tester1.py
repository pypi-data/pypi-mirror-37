import fcntl
import os, time

FILE = "test.txt"

with open(FILE, 'w') as fout:
	fout.write('Hello World!')

print('write done')

time.sleep(10)

print('sleep done')

with open(FILE, 'w') as fout:
	print('1')
	fcntl.flock(fout.fileno(), fcntl.LOCK_EX)