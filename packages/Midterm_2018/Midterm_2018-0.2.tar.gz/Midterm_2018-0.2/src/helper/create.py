#!/usr/bin/python
'''This file takes in date and outputs it to csv file in the directory

'''

import csv

def file_maker(out, name):
    '''Take inforamtion and make csv file in directory

    args: out the list of data, and name the name of the file to be made
    '''
    with open(name, 'wb') as myfile:
        writes = csv.writer(myfile, lineterminator='\n')
        for row in out:
            writes.writerow([row])
    myfile.close()

def main():
    '''This ain is unused
    '''
    pass

if __name__ == '__main__':
    main()
