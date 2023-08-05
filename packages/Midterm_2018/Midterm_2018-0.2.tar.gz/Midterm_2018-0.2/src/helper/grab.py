#!/usr/bin/python
''' This program takes in a url and outputs information of the
    table on the website to be used for documentation.

'''

import urllib


def getit(url):
    '''This method grabs a webpage and converts it into usable information.

    args: url, a website url converted to string.

    return: returns a list of the website table to be used

    Raises: No exceptions
    '''
    req = urllib.urlopen(url)
    all_data = req.read()
    req.close()
    return all_data

def main():
    '''This main is a place holder

    '''
    pass

if __name__ == '__main__':
    main()
