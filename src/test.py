import sys, glob, itertools

list_of_files = glob.glob('./csv/*.csv')
arr = []

for file_name in list_of_files:
  rows = list(open(file_name, 'r'))[7:]
  for row in rows:
    row = row.split(',')[0]
    arr.append(row)

print(arr)
print(len(arr))
# return arr