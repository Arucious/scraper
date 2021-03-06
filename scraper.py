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
from bs4 import Comment
from urllib2 import urlopen
from urllib import urlretrieve
from urlparse import urljoin
import re
#from pexpect import run, spawn

def main ():

    global options, args
    # put webpage url here
    # example: http://thedailywag.tumblr.com/
    webpage = "http://thedailywag.tumblr.com/" # TODO change to command line arg

    # put directory on pc where you want to store images
    # example: "C:\Users\aruci\Documents\scrape_output"
    directory = "C:/Users/aruci/Documents/scrape_output/" # test directory TODO change to command line arg

    soup = BeautifulSoup(urlopen(webpage), "html.parser")

    # let's not be hasty--and make sure that the number of images we have does not go beyond a certain
    imageCount = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    if imageCount > 50:
        sys.exit("You have exceeded fifty files in the directory")

    # this block of code prevents us from searching for img tags that may exist within comments
    imgs = soup.find_all('img')
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment_soup = BeautifulSoup(comment)
        imgs.extend(comment_soup.findAll('img'))

    # go through all images on the page
    i = 0;
    # regex to match extension of a file
    regex = re.compile(r"\.{1}(\w*)")
    for img in imgs:
        if i > 50:
            break
        img_url = urljoin(webpage, img['src'])
        file_name = img['src'].split('/')[-1]
        # these file names are unwieldy, we can do better
        # pull extension from the current file name
        extension = regex.search(file_name).group()
        # create a new name that is image, followed by an index, and then the original extension
        # keeping extensions is how you ensure compatibility
        name = ("image_%d" + extension) % i
        file_path = os.path.join(directory, name)
        urlretrieve(img_url, file_path)
        # increase index by one for next run of for loop.
        i += 1

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