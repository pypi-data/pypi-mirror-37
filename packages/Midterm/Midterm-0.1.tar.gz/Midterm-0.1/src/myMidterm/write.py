#!/usr/bin/python
'''Wrtie list values to .csv file.
'''
import csv

def writeCSV(list):
    ''' Write a list of values to a csv file

    '''
    size = len(list)-1
    x = 0
    with open("ECSU.csv", "w+")as f:
        while x<size:
            f.write(list[x]+", ")
            f.write(list[x+1]+", ")
            f.write(list[x+2]+", ")
            f.write(list[x+3]+", ")
            f.write("\n")
            x+=4
    f.close()
    if open("ECSU.csv", "rb"):
        return 0
    else:
        return 1