from django.test import TestCase

# Create your tests here.

a = [1,2,3]
b = map(lambda i: i*2,a)
print(list(b))

c = {1: 2, 2: 3}
print(c.values())
for i in c.keys():
    c[i] = c[i] * 2
print(c)

d = [1, 2, 3]
print(d*0)