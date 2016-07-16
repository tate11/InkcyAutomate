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

# Add a row to difference.csv with
# <a href="http://www.fp-ink.info/en/details/ .ink"><img src="http://www.fp-ink.info/colorcard/ .png"></a>
# and the correct numbers for that ink 
# eg <a href="http://www.fp-ink.info/en/details/224.ink"><img src="http://www.fp-ink.info/colorcard224.png"></a>
# (this will be used as Product Content/Description)

# Add a row to difference.csv with the correct color for that ink

#(for me: learn how to merge different branches from helpful coders into the main file and read more Python books)

# Close files
file1.close()
file2.close()
theresults.close()