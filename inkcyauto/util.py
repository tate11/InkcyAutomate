"""
Misc. utility functions.
"""

def get_filepath(base, path):
    """
    Returns an absolute filepath.

    If the given path is relative it is returned as an absolute path relative to
    the base provided.
    """
    if not os.path.isabs(path):
        path = os.path.join(base, path)
        path = os.path.abspath(path)
    return path

def print_help():
    """
    Print application CLI help message.
    """
    print 'inkcyauto -f <file_directory> -i <image_directory> -w <wordpress_file> -a <airtable_file> -d <difference_file>'
    print 'Defaults:'
    print 'inkcyauto -f ./ -i Images -w goedewordpress.csv -a airtable-source.csv -d difference.csv'
    print 'All paths are relative to the file directory unless an absolute path is provided.'

