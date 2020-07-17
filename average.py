f = open("out1.txt","r")
avg = 0.0
for i in f:
	avg += float(i)
avg /= 100
print(avg)