#!/usr/bin/env python
"""Script that combine with two table/csv file by same columns.
Usage:
    python combine_files.py -f1 csv -f2 table -L gene -R GeneID -w right -o out.csv file1 file2
"""
import sys
import os
import argparse
import pandas as pd


parser=argparse.ArgumentParser(
    description='''Script that combine with two table/csv file by same columns ''',
    epilog="""hope (2019) http://tiramisutes.github.io """)
parser.add_argument("file1", help='The input left file')
parser.add_argument("file2", help='The input right file')
parser.add_argument("-f1", "--format1", choices=['csv', 'table'], help='The format of input left file')
parser.add_argument("-f2", "--format2", choices=['csv', 'table'], help='The format of input right file')
parser.add_argument("-L","--leftid", help='The column name used to combine in left file')
parser.add_argument("-R","--rightid", help='The column name used to combine in right file')
parser.add_argument("-w","--how", help='How to combine, can be: left, right, outer, inner')
parser.add_argument("-o","--output", help='The output csv file name and path')
args=parser.parse_args()

if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

#
file1 = args.file1
file2 = args.file2
ld = args.leftid
rd = args.rightid
how = args.how
output_dir = args.output

print (str(ld))

def readf(files, type):
    if type == "csv":
        df = pd.read_csv(files)
    elif type == "table":
        df = pd.read_table(files)
    return df

a=readf(file1, args.format1)
b=readf(file2, args.format2)
merge=pd.merge(left=a,right=b,left_on=ld,right_on=rd,how=how)
merge.to_csv(output_dir,index=False)

print ("The input left file is : " + file1 + "\n")
print ("The input left file is : " + file2 + "\n")
print ("The finally results file can be find in: " + output_dir + "\n")