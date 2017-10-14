def danhsach(num):
    for i in xrange(num):
        yield i

ds = danhsach(10)

for i in ds:
    print i
for j in ds:
    print j*2