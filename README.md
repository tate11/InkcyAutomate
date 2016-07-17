# InkcyAutomate
Automation script to upload new ink swatches to inkcyclopedia.com

automate.py  -- This script downloads all new images with the correct inkname to the "Images" folder in the same folder you save this script in. (new images are ones that don't match an imgur link in goedewordpress.csv).

----

# TO DO for helpful python coders:

Make difference.csv look like import-products.csv . The import-products file has the following header row: 

    id, SKU, Title, Content, Product Type, parent_id, Product Categories, Colors, brand, ink attributes, paper, nib size, Image URL

You should be able to get data from the table on fp-ink.info. The table on fp-ink.info has the following header

    Brand   Series  Name    Hue Lite    Vibrancy    L   D   Shade   Pig EG  LE  DC  Dry (s) Flow    Lubrication Bleed   Feather Ghost

----

* Find the ink on fp-ink.info, and pull information from the table for the matching row.
Either have python use the Search function on fp-ink.info and search on brandname first to get a smaller table
or just search through all 16 pages.. ( https://www.fp-ink.info/en/?page=16 is the last one at the moment  )
* I think the "Name" column should be good to search on.
* Once you've found a match, you need to access the correct row in the table
When you can access the row, you can then get the values for that cell in that row using beautifulsoup :

=== Beautifulsoup  Example on how to get data for all Columns from the table on the page (the_url) ===

Needed: this but for the specific row only that matches the ink you're looking for

    import urllib
    from bs4 import BeautifulSoup

    # the page that has the ink on it , the number at the end changes, currently goes up to 16.
    the_url = "https://www.fp-ink.info/en/?page=2" 
    
    #Beautifulsoup needs to parse the page
    r = urllib.urlopen(the_url).read().decode('utf-8')
    soup = BeautifulSoup(r, "html.parser")

    # get all Names :
    cols = [header.string for header in soup.find('thead').findAll('th')]
    namecolumn = cols.index('Name')
    name_values = [td[namecolumn].string.encode() for td in [tr.findAll('td') for tr in soup.find('tbody').findAll('tr')]]
    print name_values 

    # -- Brand
    # get all Brands :
    cols = [header.string for header in soup.find('thead').findAll('th')]
    brandcolumn = cols.index('Brand')
    brand_values = [td[brandcolumn].string.encode() for td in [tr.findAll('td') for tr in soup.find('tbody').findAll('tr')]]
    print brand_values 

    # these both work for the full table on the page.
----

* id: blank
* sku: blank (will be auto-generated on import)
* Title : ink name, same as image file name

----

* Content: if ink exists on fp-ink.info should have this format      

    `<a href="http://www.fp-ink.info/en/details/224.ink"><img src="http://www.fp-ink.info/colorcard224.png"></a>`

  	Where the number changes for each ink.
  	You should be able to use a similar process for Content and Color as we used for Names and Brands above , 
	except that those have no header name, and cols.index[0] is not working...

	The individual ink links on fp-ink.info have the following format:
    https://www.fp-ink.info/en/details/300.ink?page=13
    
    You want to keep only the 300

	-- STEP 1 
    go to matching row, get the a href link of "Details"

	I think something like this should work to get the href text so you can strip it and get the number.

        details_url = table first column .find('link', href=True)
        details_url_string = details_url.get('href')

    strip the "https://www.fp-ink.info/en/details/" from the string, and then keep only the first 1+ numbers (until you hit the . in .ink)

	-- STEP 2 store that value as 
	fpink_number =  # 300 in the example above

	Generate the text for the Content column in difference.csv :

        content = '<a href="http://www.fp-ink.info/en/details/' + str(fpink_number) + '.ink"><img src="http://www.fp-ink.info/colorcard/' + str(fpink_number) + '.png"></a>'
        print content  indeed gives the correct content, yay

----

* Product Type: simple
* parent_id : 0
* Product Categories: inks
 
---

* Colors : the correct color for that ink
 
    Current colors used are black, blue, black, blue-black, brown, burgundy, gray, green, highlighter, white, invisible/white, orange, pink, purple, red, turquoise, yellow

    The fp-ink site sometimes has blue-green where I would have both blue and green
---

*  Brand : brand_values from above beautifulsoup code

---

* ink attributes:  has to be set manually for each one.
* Paper : Neenah NEUTECH PS
* nib size: has to be set manually for each one.

---

* image URL
  
   I think I can batch upload the images into Wordpress, the problem is Wordpress will auto rename images that have the same name . I have to look into this, but don't mind manually adding these either since it's easy to see in WooCommerce which images are missing, and a good way to check if added all missing inks.


  * (ToDo for me: learn how to merge different branches from helpful coders into the main file and read more Python books)


# Suggestions welcome for more improvements.
I would like to keep code very readable (so I understand what it does), clear var names and comments for all please. 

Thank you!!



