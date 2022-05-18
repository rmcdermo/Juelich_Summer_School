n = 30
ix = range(n+1)
print("ix: ", ix)

my_sum = 0
for i in ix:
    x_new = (2.0 * i / n) - 1.0
    print("i: {:3d} -> x_new: {:+.4f}".format(i, x_new))

    if x_new >= 0:
        my_sum += x_new ** 2
    else:
        my_sum += x_new

print("my_sum: ", my_sum)