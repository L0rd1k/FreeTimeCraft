            #! /usr/bin/env python
# -*- coding: utf-8 -*-
# LIST (СПИСОК)
# Изменяем - mutable
# Содержит дублирующие элементы

powNumbers = [nmb**2 for nmb in range(10)]
print(powNumbers[0:])
powNumbers.extend(["One","Two","Three","Four"])
powNumbers.append(False)
powNumbers.remove(0)
print(powNumbers)
newlist = powNumbers.copy()

# TUPLES (КОРТЕЖИ)
# Неизменяем - immutable
# Содержит дублирующие элементы

tuples_data = (1,2,563,2,3,1,34,6,2)
print(tuples_data)
print(tuples_data.count(2))

# SET (МНОЖЕСТВО)
# Изменяем - mutable
# Содержит уникальные элементы
# Неупорядочен

t_set = {1, 343, 4, 56, 21, 1, 34, 4, 7665, 4, 32, 21}
d_set = {1,23,5,345,123,6,45,2,23,457,568,5612,312,343,21}
t_set.add(5)
t_set.update('hello')
t_set.update([21,22,23,34])
t_set.discard(34) # don't raise error if value absent
t_set.remove(343) # raise error if value absent
t_set.pop() # delete random element
print('e' in t_set)
print(t_set & d_set)
print(t_set.intersection(d_set))
print(t_set)
t_set.clear() # delete all elements
