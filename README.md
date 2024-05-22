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
After doing this, run `getImage.py` in `/pyscripts`. <br>
Now, run the script using:

```bash
flask run
```

or use debug mode.

```bash
flask run --debug
```

This should open a development server and display an IP Address. Navigate to this IP address to view _JJARQK_ Hunt

## Usage

Full documentation is found on the <a href="https://github.com/Tonnieboy300/jjarqkhunt/wiki">wiki</a>.
