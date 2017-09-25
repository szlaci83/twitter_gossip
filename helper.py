import time

now = time.localtime(time.time()-5000)
date = str(now[0]) + '-' + str(now[1]) + '-' + str(now [2])
print(now)
print(date)