import gzip, os

f_in = open('tweets.json', 'rb')
f_out = gzip.open('tweets.json.gz', 'wb')
f_out.writelines(f_in)
f_out.close()
f_in.close()
#os.remove('tweets.json')
print("done")