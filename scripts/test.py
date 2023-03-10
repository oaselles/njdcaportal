from scripts import *

# b = browser.find_elements(By.TAG_NAME, 'b')
#https://njdcaportal.dynamics365portals.us/ultra-bhi-home/ultra-bhi-propertysearch/ultra-bhi-propertyinterest?pid=02768466-6abe-44b8-ab5c-d3832c731a59
# element.send_keys("mckenziekatekramer@gmail.com")
# element = browser.find_element(By.ID, 'pass')
# element.send_keys("oGK7UKgy5uY5x0zu")
# element = browser.find_element(By.ID, 'loginbutton')
# element.click()
# time.sleep(5)
# for i in range(60):
#     print(i)
#     browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#     time.sleep(2)
# # complete = list()
# # elements = browser.find_elements(By.CSS_SELECTOR, 'i.hu5pjgll.eb18blue')
# for e in elements:
#     action = ActionChains(browser)
#     action.move_to_element(e).click().perform()
#     time.sleep(2)
#     try:
#         d = browser.find_element(By.CSS_SELECTOR, 'a[href^="https://scontent"]')
#         d.click()
#     except:
#         pass
# # get book titles
# titles = container.find_elements(By.TAG_NAME, 'a')
# for title in titles:
#     print(title.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Collects Property Data from njdcaportal')
    parser.add_argument('-city', type=str, nargs='?', default=CITY)

    params = parser.parse_args()
    print(params.city)

    CITY = params.city
    CITYDB = 'data/tables_{}.db'.format(CITY.replace(' ', '_'))
    TABLES = pd.read_pickle(CITYDB)

    df = pd.DataFrame(TABLES['PROPERTIES'])

    for t in TABLES.keys():
        df = pd.DataFrame(TABLES[t])
        o = "data/{t}_{c}.csv".format(t=t, c=CITY.replace(' ', '_'))
        df.to_csv(o,index_label='ID')

    t0 = time.time()
    print('completed in:')
    print(datetime.timedelta(seconds=time.time()-t0))