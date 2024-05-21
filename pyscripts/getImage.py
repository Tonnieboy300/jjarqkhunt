#https://api.unsplash.com/photos/random?query=food&client_id=

import json, os
from urllib import request

root = os.path.dirname(os.path.abspath(__file__))

secretKey = open(os.path.join(root, "../secrets/unsplash"), "r").read()
 
with request.urlopen(f"https://api.unsplash.com/photos/random?query=food&client_id={secretKey}") as url:
    data = json.load(url)
    open(os.path.join(root,"bgimage.json"), "w").write(json.dumps(data, indent=4))