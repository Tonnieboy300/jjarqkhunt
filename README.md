# *JJARQK* Hunt Backend
A database of restaurants in the same price range as fast food.
Made for the Spring 2023-2024 IDP at the California Academy of Math and Science
<hr>

## Installation
Make sure you have Python 3 installed. <br>
Create a terminal in the directory *JJARQK* Hunt is located in. Then, make a virtual environment and activate it.
```bash
python3 -m venv .venv
source .venv/bin/activate
```
For Windows:
```powershell
py -m venv .venv
.venv\Scripts\activate
```
Now install the required packages.
```bash
pip install -r requirements.txt
```
Before running, place a <a href="https://mapsplatform.google.com/">Google Maps Platform</a> key (named "gmaps", no file extension) and a MongoDB connection string (named "mongoDB", no file extension) in a "secrets" folder in root. <br>
Now, run the script using:
```bash
flask run
```
or use debug mode.
```bash
flask run --debug
```

## Usage

When the server is running, open the provided ip address and add "/data/search". This path provides a JSON file containing search results from passed URL arguments.

### Search

Here's an template URL:

```
[ip address or domain name]/data/search?addr=[address or coordinates]&dist=[radius to search, in meters]&tags=[tags]
```
Tags are optional, but a 400 error will occur if addr or dist are omitted. <br>

Results are returned in JSON. Here's an example:
```json
{
  "resultsFound": 3,
  "lat": 53.3511781,
  "long": -6.260969,
  "addr": "O'Connell Street Upper, North City, Dublin, Ireland",
  "maxDist": 5000,
  "results": [
    {
      "_id": {
        "$oid": "662c46a4ef384f2b3877d446"
      },
      "name": "The Spire",
      "address": "Dublin",
      "location": {
        "type": "Point",
        "coordinates": [
          -6.260251824915252,
          53.34981854814901
        ]
      },
      "tags": [
        "american",
        "burgers"
      ],
      "desc": "A modern New American burger joint. Has a cool metal pole"
    }
  ]
}
```


