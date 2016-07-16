# Ink image scraping from Klundtasaur's Airtable
# https://airtable.com/shrF8Vr0O5VPB6ZoR/tblp9rsxx6AsHwOzW/viw42CNIgWnLe5NSl

import csv
import os
import urllib
 
# Download CSV file from source and save as airtable-source.csv
# https://s3.amazonaws.com/airtable-csv-exports-production/85ae40fcf90f305273c19039ae5694a1/Table%201-Main%20View.csv

atcsv = urllib.URLopener()
atcsv.retrieve("https://s3.amazonaws.com/airtable-csv-exports-production/85ae40fcf90f305273c19039ae5694a1/Table%201-Main%20View.csv", "airtable-source.csv")

# Generate the difference.csv file
 
 #file1 is the short one
 #file2 is the long one

#thanks to hotpotatobeans for this part :)
def import_csv(filename):
    with open(filename) as file:
        # DictReader returns a generator, which would've been exhausted
        # on line 15
        return tuple(csv.DictReader(file))


def main():
    file1 = import_csv('goedewordpress.csv')
    file2 = import_csv('airtable-source.csv')

    uniq_images = set(i['Imgur Address'] for i in file2) - set(i['Imgur Address'] for i in file1)
    with open('difference.csv', 'wb') as file:
        writer = csv.DictWriter(file, ('Name', 'Status','Donated by','Inkbot version','Imgur Address','Brand+ink regex','Automod rule'))
        writer.writerows(i for i in file2 if i['Imgur Address'] in uniq_images)

if __name__ == '__main__':
    main() 

# remove all empty rows and entries that have no imgur URL
raw_input("Remove rows that have no imgur URL, then press Enter to continue...")    

theresults = file("difference.csv", 'rb')
theresultsfile = csv.reader(theresults)

for currentrow in theresultsfile :
    # Download all images and give them the correct name
    imagelink = currentrow[4]
    name = str(currentrow[0])
    fullpath = os.path.join("D:/InkCyclopedia/todo/" + name +".jpg")
    image = urllib.URLopener()
    image.retrieve(imagelink, fullpath)
    

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
 

# Close files

theresults.close()
