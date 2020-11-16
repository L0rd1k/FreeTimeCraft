a = [1,2,3,4,5]
b = [1.2, 1.4, 1.5, 0.5, 1.92]
c = 'abcde'

result = zip(a, b, c)
# LIST --> ZIP
# print(list(result))
col1,col2,col3=zip(*result)
print(col2)
