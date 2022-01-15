"""Converts a single column of a CSV file to a text file."""

# how to use:
#
# python csv_to_txt.py epilepticfit.csv -ch 3
# -ch = the EEG channel number


import argparse
import csv
import random


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
        try:
            col = getColumnFromCSV(f, coln)
            scaledCol = scaleArray(col, 1)
            l.append(scaledCol)
        except:
            break
        coln += 1
    return l


def writeFile(l):
    with open('output.txt', 'w') as f:
        for i in l:
            f.write(str(i))
            f.write('\n')


if __name__ == '__main__':

    # arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument("fileCSV", help = "The Physiobank CSV file.", type = str)
    parser.add_argument("-ch", "--channel", default = 0, help = "EEG Channel number.", type = int)
    args = parser.parse_args()

    #CSVFile = "CHB-MIT_chb23_09.csv"

    # setup
    CSVFile = args.fileCSV
    channel = args.channel

    names = getNamesFromCSV(CSVFile)
    biosignal = getBioSignals(CSVFile)[channel]
    name = getNamesFromCSV(CSVFile)[channel]
    writeFile(biosignal)
    print(name + ": " + str(len(biosignal)) + " samples written!")
