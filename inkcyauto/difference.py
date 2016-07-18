"""
Handles calculating and writing out the merged difference file.
"""
import csv

def calculate_differences(base_file, new_file, match_field=None):
    """
    Calculate the differences between two CSV files matching on a field.

    If not privided the match field is 'Imgur Address' this is not specified in
    the method signature to avoid multiple invocations sharing the same object.

    See:
    http://docs.python-guide.org/en/latest/writing/gotchas/
    """
    if not match_field:
        match_field = 'Imgur Address'
    # Calculate a set of unique values in the given matching field. Then select
    # items from the new file that are in the set of unique values and their
    # value is not the empty string.
    unique_image_urls = set(i[match_field] for i in new_file) - set(i[match_field] for i in base_file)
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
            row = {
                '#id': '',
                'SKU': '',
                'Title': item['Name'],
                'Content': '',
                'Product Type': 'ink',
                'parent_id': 0,
                'Product Categories': '',
                'Colors': '',
                'brand': '',
                'ink attributes': '',
                'paper': 'Neenah NEUTECH PS',
                'nib size': '',
                'Image URL': ''
            }
            file_writer.writerow(row)
