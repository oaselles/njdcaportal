import pandas as pd
import os
import time
import datetime
import random
import argparse
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

# input
URL = 'https://njdcaportal.dynamics365portals.us/ultra-bhi-home/ultra-bhi-propertysearch'
CITY = 'NEW BRUNSWICK CITY'
FIELDS = [
    'Registration',
    'Property Name ',
    'Building Street Address',
    'Primary Owner Name ',
    'Municipality',
    'County',
    'Block',
    'Lot',
    'ZipCode'
]

def WAIT(min_secs=2, max_secs=5):
    """Waits for a random number of seconds."""
    secs = random.randint(min_secs, max_secs)
    print('waiting', secs, 'secs')
    time.sleep(secs)
