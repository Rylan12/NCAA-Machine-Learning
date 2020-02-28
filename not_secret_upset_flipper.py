import csv

if __name__ == '__main__':
    with open('datafile1.csv', 'r') as f:
        reader = csv.reader(f)
        with open('datafile.csv', 'w') as f:
            writer = csv.writer(f)
            for row in reader:
                if row[0] == '2019' and (row[2] == '0' or row[2] == '1'):
                    row[2] = str((int(row[2]) + 1) % 2)
                writer.writerow(row)
