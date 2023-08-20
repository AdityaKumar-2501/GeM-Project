import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



def get_title(soup):
    
    try:
        # Outer Tag Object
        title = soup.find("div",class_="brand").decompose()
        title = soup.find("span",class_="model").decompose()
        title = soup.find("h1", attrs={"class":'like-h3'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

def get_brand(soup):
    try:
        # Outer Tag Object
        title = soup.find("sup").decompose()
        title = soup.find("span", attrs={"class":'brand-name'})        
        
        # Inner NavigatableString Object
        title_value = title.text
        # Title as a string value
        title_string = title_value.strip()
        # print(title_value)

    except AttributeError:
        title_string = ""

    return title_string

def get_dimensions(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class":'model'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()
        # print(title_value)

    except AttributeError:
        title_string = ""

    return title_string

def get_price(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class":'m-w'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

def get_Min_Qty_perConsignee(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class":'moq_data'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


def get_availablity(soup):
    try:
        # Outer Tag Object
        title = soup.find("strong", attrs={"class":'green'})
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

def get_seller(soup):
    try:
        head = "https://mkp.gem.gov.in"

        # Outer Tag Object
        title = soup.find("div", attrs={"class":'other-sellers-info'}).find('a')["href"]
        temp = head+title
        
        new_webpage = requests.get(temp)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        table = new_soup.find("table")

        # then we can iterate through each row and extract either header or row values:
        d = {"Header":[], "Row":[]}
        header = []
        rows = []
        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                header = [el.text.strip() for el in row.find_all('th')]
            else:
                rows.append([el.text.strip() for el in row.find_all('td')])

        # print(rows)

        d["Header"].append(header)
        d["Row"].append(rows)


    except AttributeError:
        d = ""

    return d


if __name__ == '__main__':

    d = {"Title": [], "Brand": [], "Dimensions":[], "Price": [], "Min. Qty. Per Consignee":[], "Availablity":[], "Seller":[]}

    books = []
    for i in range(1,2):
        url = f"https://mkp.gem.gov.in/handloom-cotton-gauze/search#/?q[]=gauze&page={i}&_xhr=1"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        head = "https://mkp.gem.gov.in"

        links_list = []

        links = soup.find_all('div',class_ = "variant-desc")
        for link in links:
            link = link.find('a')["href"]
            temp = head+link
            links_list.append(temp)

        for link in links_list:
            new_webpage = requests.get(link)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            # print(link)
            d["Brand"].append(get_brand(new_soup))
            d["Dimensions"].append(get_dimensions(new_soup))
            # REMEMBER to run get_title after get_brand and get_dimensions
            d['Title'].append(get_title(new_soup))
            d["Price"].append(get_price(new_soup))
            d["Min. Qty. Per Consignee"].append(get_Min_Qty_perConsignee(new_soup))
            d["Availablity"].append(get_availablity(new_soup))
            d["Seller"].append(get_seller(new_soup))
           
        
        df = pd.DataFrame.from_dict(d)
        df['Title'].replace('', np.nan, inplace=True)
        df = df.dropna(subset=['Title'])
        df.to_csv("data.csv", header=True, index=False)
            





    # for testing purposes

    # new_webpage = requests.get("https://mkp.gem.gov.in/handloom-cotton-gauze/handloom-cotton-gauze-18-meter-x-60-centimeter/p-5116877-94989474214-cat.html#variant_id=5116877-94989474214")
    # new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    # print(get_brand(new_soup), get_dimensions(new_soup))