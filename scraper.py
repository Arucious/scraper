#!/usr/bin/env python
"""
SYNOPSIS

    TODO scraper [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

EXAMPLES

EXIT STATUS

AUTHOR

    Arslan Tarar <arucious@gmail.com>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

import optparse
import os
import os.path
import sys
import time
import traceback
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
#from pexpect import run, spawn

def main ():

    global options, args
    # put webpage url here
    # example: http://thedailywag.tumblr.com/
    webpage = "" # TODO change to command line arg

    # put directory on pc where you want to store images
    # example: "C:\Users\aruci\Documents\scrape_output"
    directory = "C:\\Users\\aruci\\Documents\\scrape_output" # test directory TODO change to command line arg

    soup = BeautifulSoup(urlopen(webpage), "html.parser")

    # let's not be hasty--and make sure that the number of images we have does not go beyond a certain
    imageCount = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    if imageCount > 50:
        sys.exit("You have exceeded fifty files in the directory")
    # this block of code prevents us from searching for img tags that may exist within comments
    imgs = soup.find_all('img')
    comments = soup.findAll(text=lambda text: isinstance(text, BeautifulSoup.Comment))
    for comment in comments:
        comment_soup = BeautifulSoup(comment)
        imgs.extend(comment_soup.findAll('img'))

    # go through all images on the page
    for img in imgs:
        img_url = urllib.urljoin(webpage, img['src'])
        file_name = img['src'].split('/')[-1]
        file_path = os.path.join(directory, file_name)
        urllib.urlretrieve(img_url, file_path)

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        main()
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)