from pprint import pprint
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')
import requests
from bs4 import BeautifulSoup

h = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

BASE_URL = "https://www.myauto.ge/ka/s/00/0/00/00/00/00/00/00/avtomobilebi?stype=0&currency_id=3&det_search=0&ord=7&keyword=&category_id=m0&page="
all_cars = []

p = 1
for page in range(1, 10):
    
    r = requests.get(BASE_URL + str(page), headers = h)

    soup = BeautifulSoup(r.text, "html.parser")
    
    #  ---parsing---
    # find announcement area
    data = soup.find("div", {"class":"search-lists-container"})
    # find each announcement and get array
    rows = soup.find_all("div", {"class": "current-item"})

    

    for index, row in enumerate(rows, 1):
        obj = {}
        # searching in rows in rows
        title = row.find("h4").text.strip()
        year = row.find("p", {"class":"car-year"}).text.strip()
        engine = row.find("div", {"data-info":"ძრავი"}).text.strip()
        millage = row.find("div", {"data-engin":"გარბენი"}).text.strip()
        transmission = row.find("div", {"data-gas":"საწვავი"}).text.strip()
        wheel = row.find("div", {"data-wheel":"საჭე"}).text.strip()

        # prices = row.find_all("span", {"class":"car-price"})
        # priceInGel = prices[0].text.strip()
        # priceInUsd = prices[1].text.strip()


        # print(f"{index} {title} - {priceInGel} - {priceInUsd}")

        obj = {
            "index":index,
            "სათაური": title,
            # "ფასი ლარში": priceInGel,
            # "ფასი დოლარში": priceInUsd,
            "გამოშვების წელი": year,
            "ძრავი": engine,
            "გარბენი": millage,
            "გადაცემათა კოლოფი": transmission,
            "საჭე": wheel,
        }
    
        # write in csv
        all_cars.append(obj)
    
    p = p+1
    print (p)

with open("cars.csv", "w", encoding = "UTF-8") as f:
    wr = csv.DictWriter(f, delimiter="\t",fieldnames=list(all_cars[0].keys()))
    wr.writeheader()
    wr.writerows(all_cars)
  
pprint(all_cars)

print(f"scraping done for {p} pages")


