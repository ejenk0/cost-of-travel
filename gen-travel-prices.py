from datetime import datetime
import json, xlsxwriter, fuelprice
from matplotlib import markers
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates

with open('info.json', 'r') as f:
    info = json.load(f)

locations = info["locations"]
vehicles = info["vehicles"]

fuelprices = fuelprice.getBestFuelPrices()

# # Create Excel Document
workbook = xlsxwriter.Workbook("TravelPrices.xlsx")

displaysheet = workbook.add_worksheet("Display")
fuelsheet = workbook.add_worksheet("Fuel Data")

bold = workbook.add_format({'bold': True})
h1 = workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center'})
h2 = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center'})
h3 = workbook.add_format({'bold': True, 'font_size': 12, 'align': 'center'})
moneyformat = workbook.add_format({'num_format':'$#,##0.00'})


# Create fuel sheet
for col, fueltype in enumerate(fuelprices):
    fuelsheet.write(0, col, fueltype, bold)
    fuelsheet.write(1, col, fuelprices[fueltype]["price"])

# Create display sheet
displaysheet.write(0, 0, "Vehicle Name", h3)
displaysheet.write(1, 0, "L/100km", h3)
displaysheet.write(2, 0, "Fuel Type", h3)
displaysheet.write(3, 0, "Destination", h3)
displaysheet.set_column(0, 0, 22.5)

for col, vehicle in enumerate(vehicles, 0):
    displaysheet.merge_range(0, col*2 + 1, 0, col*2 + 2, vehicle, h1)
    displaysheet.merge_range(1, col*2 + 1, 1, col*2 + 2, vehicles[vehicle]["milage"], h2)
    displaysheet.merge_range(2, col*2 + 1, 2, col*2 + 2, vehicles[vehicle]["fuel"], h3)

    displaysheet.write(3, col*2 + 1, "One way", h3)
    displaysheet.write(3, col*2 + 2, "Return", h3)


for row, location in enumerate(locations, 4):
    displaysheet.write(row, 0, location + " (" + str(locations[location]["distance"]) + "km)")
    for col, vehicle in enumerate(vehicles):
        displaysheet.write(row, col*2 + 1, (locations[location]["distance"]/100)*vehicles[vehicle]["milage"]*(fuelprices[vehicles[vehicle]["fuel"]]["price"]/100), moneyformat)
        displaysheet.write(row, col*2 + 2, (locations[location]["distance"]/100)*vehicles[vehicle]["milage"]*(fuelprices[vehicles[vehicle]["fuel"]]["price"]/100)*2, moneyformat)
        

## Create price history chart
# Remove _fuel-info.json duplicate dates
with open('_fuel-info.json', 'r') as f:
    data = json.load(f)

seendates = []
seendata = []
newdata = {}
for timestamp in data:
    dt = datetime.fromisoformat(timestamp)
    dtstring = dt.strftime("%d/%m/%Y %H")
    if not dtstring in seendates or not data[timestamp] in seendata:
        seendates.append(dtstring)
        seendata.append(data[timestamp])
        newdata[timestamp] = data[timestamp]

with open('_fuel-info.json', 'w') as f:
    json.dump(newdata, f, indent=2)

# Plot graph
graph_data = {}

for (datestamp, entry) in newdata.items():
    for (fueltype, info) in entry.items():
        if not fueltype in graph_data.keys():
            graph_data[fueltype] = {}
        graph_data[fueltype][datetime.fromisoformat(datestamp)] = info["price"]

DONT_PLOT = ["LPG"]

fg = plt.figure()
fg.set_figwidth(10)
for (fueltype, entries) in graph_data.items():
    if not fueltype in DONT_PLOT:
        plt.plot_date(entries.keys(), entries.values(), '--o', label=fueltype, )
plt.legend(loc="center left")
plt.ylabel("Price (cents)")
plt.xlabel("Date & Time")
plt.savefig("fuelpricehistory")

displaysheet.insert_image(0, len(vehicles)*2 + 2, "fuelpricehistory.png")

workbook.close()