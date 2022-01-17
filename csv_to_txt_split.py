"""Converts a single column of a CSV file to a seperate text files 32 values each."""

# how to use:
#
# python csv_to_txt.py epilepticfit.csv -ch 3
# -ch = the EEG channel number


import argparse
import csv
import random
import os


def getNamesFromCSV(fn):
    with open(fn, 'rt') as f:
        reader = csv.reader(f)
        rows = list(reader)
        names = rows[0][1:]
    return names


def getColumnFromCSV(fn, n):
    arr = []
    with open(fn, 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                arr.append(float(row[n]))
            except:
                pass
    return arr


def scaleArray(a, s):
    temp_a = [abs(i) for i in a]
    mx = max(temp_a)
    for i in range(len(a)):
        a[i] /= mx
        a[i] *= s
        a[i] *= -1 #revert the graph so it matches the Physiobank graph
    return a


def getBioSignals(f):
    l = []
    coln = 1
    while True:
        col = getColumnFromCSV(f, coln)
        if col == []:
            break
        l.append(col)
        coln += 1
    return l


def splitAndWriteFiles(s, l, n):
    for i in range(0, len(l), n):
        arr = l[i:i+n]
        scaledArr = scaleArray(arr, 1)

        with open(s + '_' + str(i) +'.txt', 'w') as f:
            for j in scaledArr:
                f.write(str(j))
                f.write('\n')


if __name__ == '__main__':

    # arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('fileCSV', help = 'The Physiobank CSV file.', type = str)
    parser.add_argument('-ch', '--channel', default = 0, help = 'EEG Channel number.', type = int)
    args = parser.parse_args()

    # setup
    CSVFile = args.fileCSV
    channel = args.channel
    names = getNamesFromCSV(CSVFile)
    biosignal = getBioSignals(CSVFile)[channel]
    name = str(getNamesFromCSV(CSVFile)[channel][1:-1]) 

    # split the column into seperate files of 32 values each
    splitAndWriteFiles(name, biosignal, 32)


    print('Finished!')
 