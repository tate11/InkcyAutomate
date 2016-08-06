"""
Handles calculating and writing out the merged difference file.
"""
import re
import csv
import urllib
from bs4 import BeautifulSoup

def strip_str(s):
    if s is None:
        return ''
    else:
        return s.decode('utf-8').strip()

def get_fp_ink_data():
    """
    Loop through all pages of fp-ink.info and parse out their data.

    This implmentation makes assumptions about the structure of the data table
    presented by the site because some of the column headers seem to be created
    by JS at runtime.

    If the table structure changes, this implementation will not work correctly
    anymore.
    """
    base_url = 'https://www.fp-ink.info/en/?page={}'

    # Compile the URL regex so we can pull out our ID values quickly.
    id_regex = re.compile('/en/details/(?P<id_number>\d+)\.ink.*')
    # An infinite loop is used because we don't know in advance how many pages
    # of content there are to parse.
    page_number = 1
    items = []
    while True:
        url = base_url.format(page_number)
        resp = urllib.urlopen(url).read().decode('utf-8')
        parse = BeautifulSoup(resp, 'html.parser')
        table = parse.find('table', {'class': 'inktable'})
        rows = table.findAll('tr')
        if len(rows) == 0:
            break
        for row in rows:
            columns = row.findAll('td')
            link = columns[0].findAll('a')[0].attrs['href']
            id_number = id_regex.search(link).group('id_number')
            item = {
                'ID': id_number,
                'Link': link,
                'Brand': strip_str(columns[1].string),
                'Series': strip_str(columns[2].string),
                'Name': strip_str(columns[3].string),
                'Hue': strip_str(columns[4].string),
                'Lite': strip_str(columns[5].string),
                'Vibrancy': strip_str(columns[6].string),
                'L': strip_str(columns[7].string),
                'D': strip_str(columns[8].string),
                'Shade': strip_str(columns[9].string),
                'Pig': strip_str(columns[10].string),
                'EG': strip_str(columns[11].string),
                'LE': strip_str(columns[12].string),
                'DC': strip_str(columns[13].string),
                'Dry(s)': strip_str(columns[14].string),
                'Flow': strip_str(columns[15].string),
                'Lubrication': strip_str(columns[16].string),
                'Bleed': strip_str(columns[17].string),
                'Feather': strip_str(columns[18].string),
                'Ghost': strip_str(columns[19].string)
            }
            items.append(item)
        page_number += 1
    return items

def calculate_differences(base_file_handle, new_file_handle, match_field=None):
    """
    Calculate the differences between two CSV files matching on a field.

    If not privided the match field is 'Imgur Address' this is not specified in
    the method signature to avoid multiple invocations sharing the same object.

    See:
    http://docs.python-guide.org/en/latest/writing/gotchas/
    """
    if not match_field:
        match_field = 'Imgur Address'

    # Get our CSV readers ready for the file handles provided.
    new_file = csv.DictReader(new_file_handle)
    base_file = csv.DictReader(base_file_handle)

    # Calculate a set of unique values in the given matching field. Then select
    # items from the new file that are in the set of unique values and their
    # value is not the empty string.
    unique_image_urls = set(i[match_field] for i in new_file) - set(i[match_field] for i in base_file)
    
    # Rewind the underlying new CSV so we can read through it again.
    new_file_handle.seek(0)
    unique_items = [i for i in new_file if i[match_field] in unique_image_urls and len(i[match_field].strip())]
    return unique_items

def write_difference_file(items, fp_ink_data, path):
    """
    Writes the difference file for import into WooCommerce.

    Takes the provided items and cross references them with the data scraped
    from fp-ink.info to generate complete records.
    """
    field_names = [
            '#id',
            'SKU',
            'Title',
            'Content',
            'Product Type',
            'parent_id',
            'Product Categories',
            'Colors',
            'brand',
            'ink attributes',
            'paper',
            'nib size',
            'Image URL'
            ]
    with open(path, 'wb') as file_handle:
        file_writer = csv.DictWriter(file_handle, fieldnames=field_names)
        file_writer.writeheader()
        for item in items:
            fp_item = [i for i in fp_ink_data if (i['Brand'] + ' ' + i['Name']) == unicode(item['Name'], 'utf-8')]
            content = ''
            brand = ''
            colors = ''
            if len(fp_item):
                fp_item = fp_item[0]
                content = '<a href="http://www.fp-ink.info/en/details/{}.ink"><img src="http://www.fp-ink.info/colorcard{}.png"></a>'.format(fp_item['ID'], fp_item['ID'])
                brand = fp_item['Brand']
                colors = fp_item['Hue'].split('-')
                colors = ' '.join(colors)
            row = {
                '#id': '',
                'SKU': '',
                'Title': item['Name'],
                'Content': content,
                'Product Type': 'simple',
                'parent_id': 0,
                'Product Categories': 'inks',
                'Colors': colors,
                'brand': brand,
                'ink attributes': '',
                'paper': 'Neenah NEUTECH PS',
                'nib size': '',
                'Image URL': ''
            }
            file_writer.writerow(row)
