from scripts import *

# output
RECORDS = list()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Collects Property Data from njdcaportal')
    parser.add_argument('-city', type=str, nargs='?', default=CITY)

    params = parser.parse_args()
    CITY = params.city

    # create browser object
    browser = webdriver.Chrome('chromedriver_win32/chromedriver.exe')
    browser.get(URL)

    # select the city and click search
    e = browser.find_element(By.ID, 'ultra_municipality')
    select = Select(e)
    select.select_by_visible_text(CITY)
    e = browser.find_element(By.ID, 'searchBtn')
    e.click()

    WAIT()

    more = True
    while more:
        
        # find the record table
        table = browser.find_element(By.ID, 'piList')
        # get all the tr tags (rows of the table)
        trs = table.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            # iterate through tr tags (rows)
            print('-'*25)

            # find the first link in the row and get href
            l = tr.find_element(By.TAG_NAME, 'a')
            href = l.get_property('href')
            print(href)

            # links with "pid=" are links to a property
            if 'pid=' in href:
                # collect data in structured format
                record = {
                'Link': href
                }
                tds = tr.find_elements(By.TAG_NAME, 'td')
                # iterate over fields and columns
                for field, td in zip(FIELDS, tds):
                    record[field] = td.text

                RECORDS.append(record)

        # look for disabled buttons
        nn = browser.find_elements(By.CLASS_NAME, 'disabled')
        if nn:
            # if there are any, do they say Next
            if nn[0].text=='Next':
                # if so then there are no more, this will stop iterations
                more = False
        try:
            # try to click text (will fail if not there)
            n = browser.find_element(By.LINK_TEXT, 'Next')
            n.click()
        except:
            pass

        # after waiting if more = True, will collect more data
        WAIT()

    DATASET = pd.DataFrame(RECORDS)
    DATASET.to_csv('records/prop_records_{}.csv'.format(CITY.replace(' ','_')), index_label='UPID')