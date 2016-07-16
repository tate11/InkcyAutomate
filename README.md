# InkcyAutomate
Automation script to upload new ink swatches to inkcyclopedia.com

automate.py  -- This script downloads all new images (compared to wordpress.csv file, looking at unique imgur links) to my local harddisk, with the correct inkname.

I then run the images through 2 Photoshop Droplets that cut out swatches and resize them.
The Swatch image is the Product image, the smaller one is the second product image.

# TO DO for helpful python coders:

Make difference.csv look like import-products.csv
The CSV file has the following header row: 

    id, SKU, Title, Content, Product Type, parent_id, Product Categories, Colors, brand, ink attributes, paper, nib size, Image URL

* id: blank
* sku: blank (will be auto-generated on import)
* Title : ink name
* Content: if ink exists on fp-ink.info should have this format  
    
    

    `<a href="http://www.fp-ink.info/en/details/ .ink"><img src="http://www.fp-ink.info/colorcard/ .png"></a>
    with the correct numbers for that ink on fp-ink.info (I have permission to use that website's images).
    eg <a href="http://www.fp-ink.info/en/details/224.ink"><img src="http://www.fp-ink.info/colorcard224.png"></a>`

*  Product Type: simple
* parent_id : 0
* Product Categories: inks
* Colors : the correct color for that ink
 
    Current colors used are black, blue, black, blue-black, brown, burgundy, gray, green, highlighter, white, invisible/white, orange, pink, purple, red, turquoise, yellow

    The fp-ink site sometimes has blue-green where I would have both blue and green

* Brand
    
    Current brands used are Akkerman, Aurora, Blackstone, Caran d'Ache, Conway Stewart, Cross, De Atramentis, Diamine, Faber-Castell, Franklin Christoph, J Herbin, Kaweco, KWZ, Lamy, Levenger, Montblanc, Montegrappa, Monteverde, Noodler's, Organics Studio, Parker, Pelikan, Pilot, Platinum, Private Reserve, Rohrer & Klingner, Sailor, Sheaffer, Stipula, Toucan, Visconti, Waterman

* ink attributes:  has to be set manually for each one.
* Paper : Neenah NEUTECH PS
* nib size: has to be set manually for each one.
* image URL
  
   I think I can batch upload the images into Wordpress, the problem is Wordpress will auto rename images that have the same name . I have to look into this, but don't mind manually adding these either since it's easy to see in WooCommerce which images are missing, and a good way to check if added all missing inks.


  * (ToDo for me: learn how to merge different branches from helpful coders into the main file and read more Python books)


CSV file to be imported into WooCommerce has this format: *import-products.csv*

# Suggestions welcome for more improvements.
I would like to keep code very readable (so I understand what it does), so there is no need to optimize/minimize it into gobbledygook, clear var names for all please.

Thank you!!



