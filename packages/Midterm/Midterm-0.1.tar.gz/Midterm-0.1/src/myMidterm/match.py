#!/usr/bin/python
'''Extract html table data from webpage.
'''
import urllib2
from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution
import re

def regex_match(url='http://www.ecsu.edu/faculty-staff/profiles/index.html'):
    ''' Extract html code from url

    Returns:
        match_list: list containing html table elements
    '''
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    match_list = []
    pattern = re.compile(r'td>(.*?)</td')
    parsed_html = BeautifulSoup(html, "lxml")
    for val in re.findall(pattern, str(parsed_html)):
        match = re.search('\">(.*?)</a>', val)
        if match:
            match_list.append(str(match.group(1)).replace(',', ''))
        else:
            match_list.append(str(val).replace(',', ''))
    return match_list