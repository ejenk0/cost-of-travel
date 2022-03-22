from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup as bs

def getBestFuelPrices():
    soup = bs(requests.get('https://refinery.fyi').text, 'html.parser')

    entries = soup.find_all(class_='fuel__item--active')

    fuelinfo = {}
    for i in entries:
        fuelinfo[i.find(class_="fuel__type").get_text()] = {
            "location": i.find(class_="fuel__location").get_text().replace("\u00a0", " "),
            "coords": [float(e.strip()) for e in i.find(class_="fuel__coordinates")["value"].split(",")],
            "price": float(i.find(class_="fuel__price").get_text()),
            }

    with open("_fuel-info.json", "r") as f:
        data = json.load(f)

    data[datetime.isoformat(datetime.now())] = fuelinfo

    with open("_fuel-info.json", "w") as f:
        json.dump(data, f, indent=2)
    
    return fuelinfo
