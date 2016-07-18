"""
Handles downloading resources.
"""
import os
import sys
import urllib
import multiprocessing

def download_airtable_csv(path):
    """
    Download Klundtasaur's Airtable ink table.

    Presently non-functional. You must download the CSV directly from 
    https://airtable.com/shrF8Vr0O5VPB6ZoR/tblp9rsxx6AsHwOzW/viw42CNIgWnLe5NSl
    and save it in an accessible location.

    The download method provided below is kept for historical purposes and in
    hope of eventually fixing it.
    """
    if True:
        print 'Automatic download is currently not working. Please download the CSV directly from Airtable and save locally.'
        print 'Expected path: {}'.format(path)
    else:
        airtable_url = 'https://s3.amazonaws.com/airtable-csv-exports-production/b82da440462b15aade5a2ca1705aeef3/Table%201-Main%20View.csv'
        airtable_csv = urllib.URLopener()
        try:
            airtable_csv.retrieve(airtable_url, path)
        except Exception as error:
            print error
            sys.exit(2)

def download_images(items, destination_path):
    """
    Download all images and rename them.

    Returns a list of images that failed to download.

    Note: Multiprocessing has been used to speed up the downloads by executing
    them in parallel. For more information reference the documentation at:
    https://docs.python.org/2/library/multiprocessing.html
    """
    process_pool = multiprocessing.Pool()

    image_data = [(os.path.join(destination_path, item['Name'].strio() + '.jpg'), item['Imgur Address']) for item in items]
    results = process_pool.map(download_image, image_data)
    return [x for x in results if len(x)]

def download_image((image_path, image_url)):
    """
    Downloads a single image to a file.
    """

    if os.path.exists(image_path):
        return ''

    print 'Downloading file: {}'.format(image_path)
    
    try:
        image = urllib.URLopener()
        image.retrieve(image_url, image_path)
        return ''
    except:
        return image_path + '-' + image_url
