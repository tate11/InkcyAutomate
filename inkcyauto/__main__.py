"""
"""
import os
import sys
import time
import getopt
import csv

from difference import calculate_differences
from difference import write_difference_file
from difference import get_fp_ink_data
from download import download_airtable_csv
from download import download_images 
from util import get_filepath
from util import print_help

# Hopefully forces UTF-8 encoding
reload(sys)
sys.setdefaultencoding('utf-8')

def main(argv):
    """

    """

    file_directory = './'
    image_directory = 'images'
    wordpress_file = 'wordpress.csv'
    airtable_file = 'airtable.csv'
    difference_file = 'difference.csv'

    # Process any commandline options provided.
    try:
        opts, args = getopt.getopt(argv, 'hw:a:d:f:i:', ['help', 'wordpress=', 'airtable=', 'difference=', 'filedir=', 'imagedir='])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    if len(opts) == 0:
        print 'Using default parameters...'
    else:
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print_help()
                sys.exit()
            elif opt in ('-w', '--wordpress'):
                wordpress_file = arg
            elif opt in ('-a', '--airtable'):
                airtable_file = arg
            elif opt in ('-d', '--difference'):
                difference_file = arg
            elif opt in ('-f', '--filedir'):
                file_directory = arg
            elif opt in ('-i', '--imagedir'):
                image_directory = arg

    # Generate absolute file paths for the application to work with.
    file_directory = os.path.abspath(file_directory)
    image_directory = get_filepath(file_directory, image_directory)
    wordpress_file = get_filepath(file_directory, wordpress_file)
    airtable_file = get_filepath(file_directory, airtable_file)
    difference_file = get_filepath(file_directory, difference_file)

    # Print out the current settings:
    print 'Base Directory: {}'.format(file_directory)
    print 'Image Directory: {}'.format(image_directory)
    print 'Wordpress CSV: {}'.format(wordpress_file)
    print 'Airtable CSV: {}'.format(airtable_file)
    print 'Difference CSV: {}'.format(difference_file)

    # Check that the current environment is sane.
    try:
        assert os.path.exists(file_directory), 'Base file path does not exist!'
        assert os.path.exists(image_directory), 'Image directory path does not exist!'
        assert os.path.exists(wordpress_file), 'Wordpress CSV not found!'
    except AssertionError as error:
        print error
        sys.exit(2)

    start_time = time.time()
    
    try:
        print 'Retrieving Airtable CSV...'
        download_airtable_csv(airtable_file)
        assert os.path.exists(airtable_file), 'Airtable CSV not found!'
    except AssertionError as error:
        print error
        sys.exit(2)
    print 'Airtable file ready!'

    try:
        print 'Retrieving fp-ink.info data...'
        fp_ink_data = get_fp_ink_data()
    except Exception as error:
        print error
        sys.exit(2)
    print 'fp-ink.info data ready!'

    print 'Importing source CSVs...'
    with open(wordpress_file) as wordpress_file_handle, open(airtable_file) as airtable_file_handle:
        print 'Calculating differences...'
        new_items = calculate_differences(wordpress_file_handle, airtable_file_handle)

        print 'Writing differences out to file...'
        write_difference_file(new_items, fp_ink_data, difference_file)

        print 'Downloading new images...'
        failed_images = download_images(new_items, image_directory)

        if len(failed_images):
            print 'The following images failed to download:\n{}'.format('\n'.join(failed_images))

        print 'Script completed in: {}s'.format(time.time() - start_time)

if __name__ == '__main__':
    main(sys.argv[1:])
