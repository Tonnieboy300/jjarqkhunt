#https://api.unsplash.com/photos/random?query=food&client_id=

import json
from urllib import request

secretKey = open("../secrets/unsplash", "r").read()
 
with request.urlopen(f"https://api.unsplash.com/photos/random?query=food&client_id={secretKey}") as url:
    data = json.load(url)
    open("./bgimage.json", "w").write(json.dumps(data, indent=4))