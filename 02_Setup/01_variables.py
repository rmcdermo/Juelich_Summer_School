# simple assignment
a = 70
b = 70*4.5
c = b ** 0.5

# print unformatted
print(a, b, c)

# formatted print
print("values of a: {}, b: {}, c: {}".format(a,b,c))

# create empyt list, via [], append values to it
alist = []
alist.append(a)
alist.append(4.5)
alist.append(10)

# read and assign list's elements
alist[2] = alist[0] * 3

# print the list
print(alist)