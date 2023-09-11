# mine for apartments and save
# beautiful soup
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

# create dataframe
df = pd.DataFrame(columns=['Price', 'Beds', 'Baths', 'Sq ft', 'Street', 'City', 'Zip'])

# process a single listing card into a dictionary for dataframe
def process_html(div):
    # add to csv
    data = div.split('\n')
    print(data)
    # data[2] has addr
    data_idx = 2
    for i in range(len(data)):
        if "Favorite" in data[i]:
            data_idx = i
    addr = data[data_idx].split("Favorite")[1].split(',')
    addr_street = addr[0].strip(' ')
    addr_city = addr[1].strip(' ')
    addr_zip = addr[2].strip(' ')[2:]

    # data[3] has price
    price = data[data_idx+1].strip(' ')
    # data[4] has beds/baths/sqft
    additional = data[data_idx+2].split('Listing')[0]
    additional = additional.split(' ')
    beds, baths, sqft = None, None, None
    for idx, item in enumerate(additional):
        if item == 'Beds':
            beds = additional[idx-1]
        elif item == 'Baths':
            baths = additional[idx-1]
        elif item == 'Sq':
            sqft = additional[idx-1]
    new_row = {'Price' : price, 'Beds' : beds, 'Baths' : baths, 'Sq ft' : sqft, 'Street' : addr_street, 'City' : addr_city, 'Zip' : addr_zip}
    return new_row


# there are 12 pages to store each page url in a list
pages = ["https://www.remax.com/homes-for-rent/oh/columbus/the-ohio-state-university/neighborhood/54258?filters={%22locationRect%22:{%22minLat%22:39.781575197499535,%22maxLat%22:40.167276527324965,%22minLon%22:-83.37336255108774,%22maxLon%22:-82.69083691632211},%22bRentalPropertyType%22:%22Rental%22,%22freeSearch%22:true}"]
page_count = 11
for i in range(page_count):
    page_root = "https://www.remax.com/homes-for-rent/oh/columbus/the-ohio-state-university/neighborhood/54258/page-"
    page_suffix = "?filters={%22locationRect%22:{%22minLat%22:39.781575197499535,%22maxLat%22:40.167276527324965,%22minLon%22:-83.37336255108774,%22maxLon%22:-82.69083691632211},%22bRentalPropertyType%22:%22Rental%22,%22freeSearch%22:true}"
    pages.append(page_root + str(i) + page_suffix)

# for each stored page, get data, process, place into df
for page in pages:
    response = requests.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    mydivs = soup.find_all("div", {"class": "listings-card"})
    for div in mydivs:
        data = process_html(div.text)
        df.loc[len(df)] = data
    sleep(10)

# save df data
df.to_csv("ohio_rentals_mined.csv")