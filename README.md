# Immoweb Scraper

![Immoweb logo (image)](https://assets.immoweb.be/122/images/logos/sharing-logo.png)

## *Description*

The script main.py , **scraping()**, includes the code to first scrape the main *immoweb.be* pages to get all urls(hrefs) for all the real-estate properties.
We have used requests to get the html.
We use multithreading with the function map to decrease processing time. We end-up with > 13K urls scraping houses, appartments, and new project houses & appartments.
We have included the new project buildings for the later steps of making a valuation model, as a new project building might be a factor in the valuation of a newproperty.

The second part of the main.py , **get_tables()**, will allow the scraping of all tables in all from all the urls collected in the first part.
We have used requests.
We are also using multithreading to gain efficiency.

Performance : running this script took and getting all the data (urls+tables) took ~15 min (might differ based on your network & computer).

## *Installation*

To run the code the following packages must be installed : requests, bs4, pandas, json and concurrent.futures .

## *Usage*

Run in a terminal *"Python3 main.py"*.

## (Visuals)
## (Contributors)
## (Timeline)
## (Personal situation)
