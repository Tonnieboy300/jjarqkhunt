# _JJARQK_ Hunt

A database of restaurants in the same price range as fast food.
Made for the Spring 2023-2024 IDP at the California Academy of Math and Science.

## Installation

Make sure you have Python 3 installed. <br>
Create a terminal in the directory _JJARQK_ Hunt is located in. Then, make a virtual environment and activate it.

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

Before running, place all required secrets into /secrets. Check /secrets/README.md for more info. <br>
Now, run the script using:

```bash
flask run
```

or use debug mode.

```bash
flask run --debug
```

## Usage

When the server is running, open the provided ip address.

### Search

This opens _JJARQK_ Hunt's web interface, which includes a search function at root. <br>

This page then redirects to /search, which includes URL arguments for each search parameter:

```
[ip address or domain name]/search?addr=[address or coordinates]&dist=[radius to search, in miles]&tags=[tags]
```

Tags are optional, but a 400 error will occur if addr or dist are omitted. <br>

For API use, this URL returns JSON.

```
[ip address or domain name]/data/search?addr=[address or coordinates]&dist=[radius to search, in miles]&tags=[tags]
```

Here's an example:

```json
{
  "resultsFound": 1,
  "lat": 53.3511781,
  "long": -6.260969,
  "addr": "O'Connell Street Upper, North City, Dublin, Ireland",
  "maxDist": 5000,
  "tags": ["american", "burgers"]
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
      "desc": "A modern New American burger joint. Has a cool metal pole",
      "website": "https://jjarqk.com"
    }
  ]
}
```

In the returned data, `"maxDist"` is in meters, as MongoDB accepts meters when searching by location.

### MongoDB
_JJARQK_ Hunt uses MongoDB to store data. It creates three collections, "restaurants", "submissions", and "auth", within a "idp11_data" database.
