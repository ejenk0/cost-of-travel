# cost-of-travel
Creates an Excel file with the costs of travelling to configured locations in configured vehicles with best live fuel and price history graph.

![image](https://user-images.githubusercontent.com/74844913/159490504-a53f702d-479f-4e11-9843-6037cd5a60ad.png)


## Usage
1. Configure `info.json` with locations and vehicles to be calculated
2. Run `gen-travel-prices.py` to generate a new `TravelPrices.xlsx` with up to date best fuel prices. (**WILL OVERWRITE `TravelPrices.xlsx`**)
3. Open `TravelPrices.xlsx` to view generated data and price history graph.

## Details
### fuelprice.py
This is the script that fetches the latest best fuel prices from across Australia from refinery.fyi for each fuel type.
It returns from the `getBestFuelPrices()` function the latest data, and stores that data in `_fuel-info.json`

### gen-travel-prices.py
This is the main script. It calls `getBestFuelPrices()` and uses the returned data in conjunction with the locations and vehicles configuration in `info.json` to calculate and display all data in `TravelPrices.xlsx`.
It also clears all entries to `_fuel-info.json` that were within the same hour as another (unless the entry is different from all others)

### info.json
This json file contains the configuratin for which locations should have their travel costs calculated along with the distance to them.
It also has the conifguration for all vehicles to be calculated along with relevant data such as the fuel type used and their fuel milage (L/100km)

It is structured as follows:
```
{
  "vehicles": {
    $vehiclename(string) : {
      "milage": $fueleffeciency(float),
      "fuel": $fueltype["U91", "P95", "P98", "E10", "DSL", "LPG"]
    },
    ...
  },
  "locations": {
    $locationname(string): {
      "distance": $distanceinkm(float)
    },
    ...
  }
}
```
