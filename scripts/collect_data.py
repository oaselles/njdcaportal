from scripts import *

# property records
PROPERTIES = list()


# related table names
RELATED_TABLES = [
    'BUILDINGS',
    'CONTACTS',
    'BILLS',
    'JUDGEMENTS',
    'UPCOMING_INSPECTIONS',
    'PREVIOUS_INSPECTIONS'
]

def get_selected_option(Br, eid):
    e = Br.find_element(By.ID, eid)
    ops = e.find_elements(By.TAG_NAME, 'option')
    for o in ops:
        if o.get_property('selected'):
            return o.text
    return None

def get_text_value(Br, eid):
    e = Br.find_element(By.ID, eid)
    return e.get_property('value')

def get_property_data(x, Br, DB):
    PROPERTY = x.to_dict().copy()

    # check if this property has already been collected
    props = pd.DataFrame(DB['PROPERTIES'])
    if not props.empty:
        if PROPERTY['Registration'] in props['Registration'].tolist():
            return 'exists'

    Br.get(x['Link'])
    print(x['Link'])
    #copy fields from property search

    PROPERTY['RegistrationPID'] = get_text_value(Br,'ultra_bhiregistrationnumber')
    PROPERTY['PropertyName'] = get_text_value(Br,'ultra_name')
    PROPERTY['PropertyType'] = get_selected_option(Br,'ultra_bhipropertyinteresttype')
    PROPERTY['Units'] = get_text_value(Br,'ultra_unitcount')
    PROPERTY['OwnershipType'] = get_selected_option(Br,'ultra_ownershiptype')
    PROPERTY['Owner'] = get_text_value(Br,'ultra_propertyowner_name')
    PROPERTY['OwnerContact'] = get_text_value(Br,'ultra_ownercontact_name')
    PROPERTY['OwnerAddress'] = get_text_value(Br,'ultra_propertyowner_address')
    PROPERTY['OwnerAgentName'] = get_text_value(Br,'ultra_bhiauthorizedagent_name')
    PROPERTY['OwnerAgentContact'] = get_text_value(Br,'ultra_aaContact_dummy')
    PROPERTY['OwnerAgentAddress'] = get_text_value(Br,'ultra_aaContactAddress_dummy')
    PROPERTY['BuildingCount'] = get_text_value(Br,'ultra_buildingcount')

    # Gathers all table data, will want to expand this process for some tables
    tables = Br.find_elements(By.CLASS_NAME, 'table')
    for name, table in zip(RELATED_TABLES, tables):
        # loop through tables found, named above
        print('collecting table records from:', name)

        # get the headers / field names
        thead = table.find_elements(By.TAG_NAME, 'tr')
        trs = table.find_elements(By.TAG_NAME, 'tr')
        fields = list()
        ths = table.find_elements(By.TAG_NAME, 'th')
        for th in ths:
            try:
                a = th.find_element(By.TAG_NAME, 'a')
                fields.append(a.text.split('\n. sort')[0])
            except:
                pass
        
        for tr in trs[1:]:
            # loop through the rows
            tds = tr.find_elements(By.TAG_NAME, 'td')
            # collect data, by fields
            row = dict()
            row['Registration'] = PROPERTY['Registration']
            for f, td in zip(fields, tds):
                row[f] = td.text
            DB[name].append(row)

    # add the Property dictionary as a record to the properties table
    DB['PROPERTIES'].append(PROPERTY)
    print('writing')
    pd.to_pickle(DB, CITYDB)
    return 'added'

if __name__ == '__main__':
    t0 = time.time()
    parser = argparse.ArgumentParser(
        description='Collects Property Data from njdcaportal')
    parser.add_argument('-city', type=str, nargs='?', default=CITY)
    parser.add_argument('-TM', type=int, nargs='?', default=5)
    parser.add_argument('--overwrite', action='store_true', default=False)
    params = parser.parse_args()
    print(params)
    CITY = params.city
    CITYDB = 'data/tables_{}.db'.format(CITY.replace(' ', '_'))
    
    if os.path.exists(CITYDB) and not params.overwrite:
        TABLES = pd.read_pickle(CITYDB)
    else:
        if not os.path.exists('data/'):
            os.mkdir('data')
        TABLES = defaultdict(list)
        pd.to_pickle(TABLES, CITYDB)

    # def collect_property_record(url):
    Br = webdriver.Chrome('chromedriver_win32/chromedriver.exe')
    
    # if the stage one records have been collected
    csv = 'records/prop_records_{}.csv'.format(CITY.replace(' ','_'))
    if os.path.exists(csv):
        df = pd.read_csv(csv)
        rs = list()
        T=1
        for i, row in df.iterrows():
            if T>params.TM:
                # over threshold append to-do
                rs.append('to-do')
            else:
                # get data
                r = get_property_data(row, Br=Br, DB=TABLES)
                rs.append(r)
                if r=='added':
                    print(T, params.TM)
                    print(pd.Series(rs).value_counts())
                    T+=1
                    WAIT()
        print(pd.Series(rs).value_counts())
    else:
        print(CITYDB, 'does not exist.')
        print('run the >>python -m scripts.collect_records.py for {}'.format(CITY))

    df = pd.DataFrame(TABLES['PROPERTIES'])

    print('completed in:')
    print(datetime.timedelta(seconds=time.time()-t0))