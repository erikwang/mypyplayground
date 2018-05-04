import csv
with open('c:\\fm.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter =',')
    for row in spamreader:
        print(', '.join(row))
