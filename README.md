# scraping property data

Scrapes property data from NJDCA portal, using Selenium and BS4. Currently only extracts property records and links, but will collect other fields for 
each property.

NJDCA portal:
https://njdcaportal.dynamics365portals.us/ultra-bhi-home/ultra-bhi-propertysearch

## setup

1. Install Conda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
2. Download a supported web driver: https://selenium-python.readthedocs.io/installation.html#drivers
2. Setup environment using Conda: `conda create --name myenv --file spec-file.txt`

Helpful documentation for using the WebDriver API https://selenium-python.readthedocs.io/index.html

Conda documentation for managing environments:
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

## usage

To collect property records and links for NEW BRUNSWICK CITY:
`python -m scripts.collect_records`

To do a different city, specify:
`python -m scripts.collect_records -city "HIGHLAND PARK BORO"`

Output is saved as a csv in the output folder. An example of the output is here:
https://docs.google.com/spreadsheets/d/1EMfypnlR0lw6XuUyPOFglQ_wWNrCN238Y-yh9DhIqW4/edit?usp=sharing



