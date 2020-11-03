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


print("Hello!")
name = input("Enter your name: "),
print("Your name is {} ".format(name[0]))