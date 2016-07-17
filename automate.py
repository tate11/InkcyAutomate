# Ink image scraping from Klundtasaur's Airtable
# https://airtable.com/shrF8Vr0O5VPB6ZoR/tblp9rsxx6AsHwOzW/viw42CNIgWnLe5NSl

import csv
import os
import urllib
import multiprocessing
from time import time
 

def retrieve_airtable(filename):
    '''
   Download CSV file from source and save as airtable-source.csv
   https://s3.amazonaws.com/airtable-csv-exports-production/85ae40fcf90f305273c19039ae5694a1/Table%201-Main%20View.csv
   this is NOT a static URL!
    

   !!!

   NOT WORKING ANYMORE  - For now you have to manually download the file from
   https://airtable.com/shrF8Vr0O5VPB6ZoR/tblp9rsxx6AsHwOzW/viw42CNIgWnLe5NSl
   (click on the three dots, then "Download CSV")
   and save it as airtable-source.csv in the same folder this script is in
   
   !!!

   '''
    airtabl_url = "https://s3.amazonaws.com/airtable-csv-exports-production/b82da440462b15aade5a2ca1705aeef3/Table%201-Main%20View.csv"
    atcsv = urllib.URLopener()
    try:
        atcsv.retrieve(airtabl_url, filename)
    except:
        assert False, "Unable to retrieve airtable file"
 
 
def import_csv(filename):
    '''
   Generate the difference.csv file
 
   file1 is the short one
   file2 is the long one
 
   thanks to hotpotatobeans for this part :)
   '''
    with open(filename) as file:
        # DictReader returns a generator, which would've been exhausted
        # on line 15
        return tuple(csv.DictReader(file))
 
 
def save_differences(filename, master_file, new_file, matching_field="Imgur Address"):
    '''
   Calculates the differences between two files and saves it to a CSV file
   '''
 
    uniq_images = set(i[matching_field] for i in new_file) - set(i[matching_field] for i in master_file)
    uniq_list = [i for i in new_file if i[matching_field] in uniq_images and len(i[matching_field].strip())]
    with open(filename, 'wb') as file:
        writer = csv.DictWriter(file, ('Name', 'Status', 'Donated by', 'Inkbot version', 'Imgur Address', 'Brand+ink regex', 'Automod rule'))
        writer.writerows(uniq_list)
    return uniq_list
 
def download_image((image_path, imagelink)):
    '''
   Downloads a single image to a file for use in the parallel map
   '''
 
    if os.path.exists(image_path):
        return ""
 
    print "Retrieving file: {}".format(image_path)
 
    try:
        image = urllib.URLopener()
        image.retrieve(imagelink, image_path)
        return ""
    except:
        return image_path + "-" + imagelink
 
def download_images(image_folder, uniq_list):
    '''
   Download all images and give them the correct name
 
   Returns a list of failed images
 
   Note: I've used multiprocessing here to download multiple images in parallel for faster processing
   if you're interested in how this works check out the documentation here:
   https://docs.python.org/2/library/multiprocessing.html
   '''
 
 
    MP_pool = multiprocessing.Pool()
 
    image_data = [(os.path.join(image_folder, item['Name'].strip() + ".jpg"), item["Imgur Address"]) for item in uniq_list]
 
    results = MP_pool.map(download_image, image_data)
 
    return [x for x in results if len(x)]
 
def main():
    file_folder = "./" # Same folder script is run from
    image_folder = "./Images" # A folder called Images inside the folder the script is in
 
    wordpress_file = os.path.join(file_folder, "goedewordpress.csv")
    airtable_file = os.path.join(file_folder, "airtable-source.csv")
    difference_file = os.path.join(file_folder, "difference.csv")
 
    assert os.path.exists(wordpress_file), "No Wordpress CSV file found"
 
    start_time = time()
 
    print "\nRetrieving Airtable file.."
    
    # has to be done manually for now
    # retrieve_airtable(airtable_file)
 
    print "\nAirtable File retrieved!"
 
    print "\nImporting CSV files..."
 
    file1 = import_csv(wordpress_file)
    file2 = import_csv(airtable_file)
 
    print "\nCSV Files imported!"
 
    print "\nSaving the file differences..."
 
    uniq_list = save_differences(difference_file, file1, file2)
 
    print "\nDifferences saved!"
 
    # THE BELOW IS NO LONGER NEEDED DUE TO THE TRY EXCEPTS IN THE DOWNLOAD LOOP
    #
    ## remove all empty rows and entries that have no imgur URL
    ## raw_input("Remove rows that have no imgur URL, then press Enter to continue...")
 
    print "\nDownloading new images..."
 
    failed_images = download_images(image_folder, uniq_list)
 
    print "\nNew Images downloaded!"
 
    if len(failed_images):
        print "\nThe following images failed to Download:\n{}".format("\n".join(failed_images))
 
    print "\nScript completed in: {}s".format(time() - start_time)
 

if __name__ == '__main__':
    main() 

 

# TO DO for helpful python coders:

# Make difference.csv look like import-products.csv
# #id,    SKU,    Title,  Content,    Product Type,   parent_id   ,Product Categories ,Colors ,brand, ink attributes, paper,  nib size,   Image URL

# -- id: blank

# -- sku: blank (will be auto-generated on import)

# -- Title : ink name

# -- Content: (if ink exists on fp-ink.info should have this format: )

# <a href="http://www.fp-ink.info/en/details/ .ink"><img src="http://www.fp-ink.info/colorcard/ .png"></a>
# with the correct numbers for that ink on fp-ink.info (I have permission to use that website's images).
# eg <a href="http://www.fp-ink.info/en/details/224.ink"><img src="http://www.fp-ink.info/colorcard224.png"></a>

# -- Product Type: simple

# -- parent_id : 0

# -- Product Categories: inks

# -- Colors : the correct color for that ink
# # Current colors used are black, blue, black, blue-black, brown, burgundy, gray, green, highlighter, white, invisible/white, orange, pink, purple, red, turquoise, yellow
# # The fp-ink site sometimes has blue-green where I would have both blue and green

# -- Brand
# # Current brands used are Akkerman, Aurora, Blackstone, Caran d'Ache, Conway Stewart, Cross, De Atramentis, Diamine, Faber-Castell, Franklin Christoph, J Herbin, Kaweco, KWZ, Lamy, Levenger, Montblanc, Montegrappa, Monteverde, Noodler's, Organics Studio, Parker, Pelikan, Pilot, Platinum, Private Reserve, Rohrer & Klingner, Sailor, Sheaffer, Stipula, Toucan, Visconti, Waterman

# -- ink attributes:  has to be set manually for each one.

# -- Paper : Neenah NEUTECH PS

# -- nib size: has to be set manually for each one.

# -- image URL
# # I think I can batch upload the images into Wordpress, the problem is Wordpress will auto rename images that have the same name
# # I will look into this, but don't mind manually adding these since it's easy to see in WooCommerce which images are missing, and a good check to see if I got all missing inks added.


# # (ToDo for me: learn how to merge different branches from helpful coders into the main file and read more Python books)

# # CSV file to be imported into WooCommerce has this format: 
# import-products.csv

# --?? Suggestions welcome for more improvements.

# -- I would like to keep code very readable (so I understand what it does), so there is no need to optimize/minimize it into gobbledygook
# -- human-readable names for all please ;)
 

