# InkcyAutomate

Automation script to upload new ink swatches to inkcyclopedia.com.

Based on and hopefully improving upon [this script by benninkcorien](https://github.com/benninkcorien/InkcyAutomate).

## Requirements

The only hard requirement is BeautifulSoup4 which you can install with.

```sh
pip install beautifulsoup4
```

Hopefully I'll have a proper setup script written shortly and you'll be able to
just use pip and get everything that you need.

## Usage

Clone down the repository and go into the project directory. You'll need to
download [Klundtasaur's Airtable list](https://airtable.com/shrF8Vr0O5VPB6ZoR/tblp9rsxx6AsHwOzW/viw42CNIgWnLe5NSl)
by hand and save it somewhere accessible. Additionally you will need a CSV of
the items currently in Wordpress saved somewhere handy. The script expects the
following defaults but each can be overridden with an appropriate commandline
flag.

```sh
File Directory: ./
Image Directory: ./images
Wordpress CSV: ./wordpress.csv
Airtable CSV: ./airtable.csv
Differences CSV: ./differences.csv

CLI Flags:
-h --help: Print help message
-w --wordpress=: Path to Wordpress CSV
-a --airtable=: Path to Airtable CSV
-d --difference=: Path to Difference CSV
-f --filedir=: Base file path
-i --imagedir=: Image directory

Usage:
python inkcyauto -w wordpress.csv -a airtable.csv -d difference.csv -f ./ -i images
```

All file paths are assumed to be relative to the base file path unless they are
specified absolutely.

## Notes
* The difference.csv output should now look just like the import-products.csv.
  However this could use some additional testing and tweaking. For example the
  Colors header is currently pulled from fp-ink.info data using it's Hue field.
