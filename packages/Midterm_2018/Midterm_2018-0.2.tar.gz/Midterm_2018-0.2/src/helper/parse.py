#!/usr/bin/python
'''PARSES data in to list from table information
'''
import re

def parser(info):
    '''Return the datasets to create CSV

    args: info is the input data from the website.

    return: these are teh data sets fro each profile

    '''
    out = []
    head = re.findall(r'<th>(.*?)</th>', str(info))
    out.append(head)
    dataset = re.findall(r'<tbody>(.*?)</tbody>', str(info), re.M|re.I|re.S)
    rows = re.findall(r'<tr>(.*?)</tr>', str(dataset), re.M|re.I|re.S)
    for row in rows:
        entries = re.findall(r'<td>(.*?)</td>', str(row), re.M|re.I|re.S)
        stuff = []
        for one in entries:
            see = striphtml(one)
            stuff.append(see)
        out.append(stuff)
    #print out
    return out

def striphtml(data):
    '''takes in html data and strips off tags

    return: returns the data after the tags have been removed.

    args: data, the raw html taht needs to be stripped
    '''
    pil = re.compile(r'<.*?>')
    return pil.sub('', data)

def main():
    '''Main is just a placeholder
    '''
    pass


if __name__ == '__main__':
    main()
