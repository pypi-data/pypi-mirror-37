# swisshydrodata

swisshydrodata is a library that allow you to get data from the [Swiss Federal Office for the Environment FOEN](https://www.hydrodaten.admin.ch/en/stations-and-data.html).
To find a station near to you, use the [list of stations](https://www.hydrodaten.admin.ch/en/stations-and-data.html) on the FEON website.

The library uses a REST API which hands out the data because the FEON does not allow to use their data service as backend.

The data update interval is limited to onece every 10 minutes by FEON, so thats how often the API has new data available.

## Example
```
from swisshydrodata import SwissHydroData 

s = SwissHydroData()

# returns a list of station numbers
s.get_stations()

# returns all data available for station #2143
s.get_station(2143)

```
