# scraping property data

## setup

Scrapes property data from NJDCA portal, using Selenium and BS4. 

NJDCA portal:
https://njdcaportal.dynamics365portals.us/ultra-bhi-home/ultra-bhi-propertysearch

1. Download a supported web driver'
2. setup environment using Conda.

Helpful documentation for using the WebDriver API https://selenium-python.readthedocs.io/index.html

Conda documentation for managing environments:
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

To create the conda environment use:

`conda create --name myenv --file spec-file.txt`

## usage

To collect property data for NEW BRUNSWICK CITY:
`python run.py`

To do a different city, specify:
`python run.py -city "HIGHLAND PARK BORO"`

Output is saved as a csv in the output folder.



