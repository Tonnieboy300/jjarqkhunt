#https://api.unsplash.com/photos/random?topics=xjPR4hlkBGA&orientation=squarish&client_id={secretKey}

import json, os
from urllib import request

root = os.path.dirname(os.path.abspath(__file__))

secretKey = open(os.path.join(root, "../secrets/unsplash"), "r").read()

# determines if a color is bright or dark
# used for the home page
def darkText(value):
    value = value.lstrip('#')
    rgb = []
    # split hex code into 3 values: r, g, b
    for char in range(len(value)):
        if char % 2 == 0:
            rgb.append(value[char])
        else:
            rgb[len(rgb)-1] = rgb[len(rgb)-1] + value[char]
    # convert values to decimal
    for val in range(len(rgb)):
        rgb[val] = (int(rgb[val], 16))/255
    lum = 0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2]
    return lum > 0.5
 
with request.urlopen(f"https://api.unsplash.com/photos/random?topics=xjPR4hlkBGA&orientation=squarish&client_id={secretKey}") as url:
    data = json.load(url)
    data.update({"dark": darkText(data["color"])})
    open(os.path.join(root,"bgimage.json"), "w").write(json.dumps(data, indent=4))