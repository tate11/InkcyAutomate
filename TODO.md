# TODO
* Python standard setup script and packaging info.
* Confirm all functionality is maintained.
* Test that output file format matches the provided import-products.csv.
* Test the fp-ink.info scraping and merge.
    * English page URLs follow the pattern: https://www.fp-ink.info/en?page=<#>
    * The table has the following headers:
        * Brand
        * Series
        * Name
        * Hue
        * Lite
        * Vibrancy
        * L
        * D
        * Shade
        * Pig
        * EG
        * LE
        * DC
        * Dry(s)
        * Flow
        * Lubrication
        * Bleed
        * Feather
        * Ghost
    * Extract the table data using BeautifulSoup and store it to a dictionary.
    * Loop through the site's pages until no rows are returned, telling us that
      we have hit the end of our data. The site doesn't seem to do anything
      except return nothing for out of range page numbers.
    * Search the resulting dictionary for for the ink name and pull its row
      data.
* Output file format
    * #id - blank
    * SKU - blank
    * Title - Name from Airtable CSV
    * Content - Link to fp-ink.info color swatch in the following format: 
      <a href="http://www.fp-ink.info/en/details/<ID>.ink"><img src="http://www.fp-ink.info/colorcard<ID>.png"></a>
        * <ID> is an integer that identifies the individual ink.
        * The Details links on the site are in the following format:
          https://www.fp-ink.info/en/details/<ID>.ink?page=<#>
    * Product Type - simple
    * parent\_id - 0
    * Product Categories - inks
    * Colors - Current colors used are black, blue, black, blue-black, brown,
      burgundy, gray, green, highlighter, white, invisible/white, orange, pink,
      purple, red, turquoise, yellow. The fp-ink site sometimes has blue-green
      where I would have both blue and green.
      * Consider splitting on dashes?
    * brand - extracted from fp-inks.info
    * ink attributes - set manually
    * Paper - Neenah NEUTECH PS
    * nib size - set manually
    * Image URL - set manually?


