import googlemaps
from flask import Flask, render_template, request, abort, session, redirect
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from werkzeug.security import check_password_hash, generate_password_hash
import certifi
from werkzeug.middleware.proxy_fix import ProxyFix
import os

root = os.path.dirname(__file__)

app = Flask(__name__)
# tells flask to not auto-sort json. helps when viewing data during testing.
app.json.sort_keys = False
app.config.from_mapping(
    SECRET_KEY=open(os.path.join(root,"secrets/secretkey"),"r").read()
)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == '__main__':
    app.run()


# init database connection
client = MongoClient(open(os.path.join(root,"secrets/mongoDB"), "r").read(),tlsCAFile=certifi.where(),connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
database = client.idp11_data
restaurants = database.restaurants
submissions = database.submissions
auth = database.auth

# init google maps api connection
maps = googlemaps.Client(key=open(os.path.join(root,"secrets/gmaps"),"r").read())

# requests for a list of locations near a set of long lat coordinates
def getSearchResults(lat: float,long: float, minDistance: int, maxDistance: int, tags: list):
    if tags:
        nearLocations = restaurants.find(
            {
                "location":{
                    "$near" : {
                        "$geometry": {"type": "Point", "coordinates": [long, lat]},
                        "$minDistance": minDistance,
                        "$maxDistance": maxDistance
                    }
                },
                "tags":{
                    "$all" : tags
                }
            }
        )
    else:
        nearLocations = restaurants.find(
            {
                "location":{
                    "$near" : {
                        "$geometry": {"type": "Point", "coordinates": [long, lat]},
                        "$minDistance": minDistance,
                        "$maxDistance": maxDistance
                    }
                }
            }
        )

    return nearLocations

# returns a list of all submissions
def getSubmissions():
    return submissions.find({})


# converts database results to JSON
# the default functions get stuck on ObjectID objects
def resultsToJSON(data):
    return json.loads(json_util.dumps(data))

@app.route('/')
def index():
    return render_template("home.html")

# generates search results from url args
# requires address (addr) and maxDistance (dist)
# optionally searches tags (tags)
def search():
    try:
        maxDistance = int(request.args.get("dist"))
    except:
        maxDistance = None

    address = request.args.get("addr")

    if (not address) or (not maxDistance):
        app.logger.error(f"Request failed from {request.remote_addr}: Error 400, Missing args, Addr {address}, maxDist {maxDistance}")
        abort(400)

    geocode_result = maps.geocode(address)

    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        long = geocode_result[0]["geometry"]["location"]["lng"]
    except IndexError:
        app.logger.error(f"Request failed from {request.remote_addr}: Could not find coordinates for address {address}")
        return [{"resultsFound":0, "lat": "error", "long": "error"}]


    tags = request.args.get("tags")
    if tags:
        # remove spaces
        tags = tags.replace(" ","")
        # splits string into a list seperated by commas
        tags = tags.split(",")

    nearLocationsData = getSearchResults(lat,long,0,maxDistance,tags)
    nearLocations = {"resultsFound":0, "lat": lat, "long": long, "addr":geocode_result[0]["formatted_address"],"maxDist":maxDistance, "tags":tags, "results":[]}

    for doc in nearLocationsData:
        nearLocations["results"].append(doc)

    nearLocations["resultsFound"] = len(nearLocations["results"])

    # app.logger.info(f"Request successful from {request.remote_addr}: Lat {lat}, Long {long}, Tags {tags}")
    return nearLocations

@app.route('/data/search')
def appSearchQuery():
    return resultsToJSON(search())

# gets all tags in the database and returns a list
# used for autofill
@app.route('/data/tags')
def getTags():
    return restaurants.distinct("tags")

@app.route('/search')
def webSearchQuery():
    results = search()
    return render_template("locations.html",tags=results["tags"],maxDistance=results["maxDist"],addr=results["addr"],locations=results["results"])

@app.route("/submit", methods=["GET", "POST"])
def submitPage(title="Submit a Restaurant"):
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form["desc"]
        addr = request.form["addr"]
        website = request.form["website"]
        #removes spaces
        tags = request.form["tags"].replace(" ","")
        #turns the tags string into a list
        tags= tags.split(",")

        geocode_result = maps.geocode(addr)

        addr = geocode_result[0]["formatted_address"]

        lat = geocode_result[0]["geometry"]["location"]["lat"]
        long = geocode_result[0]["geometry"]["location"]["lng"]

        # app.logger.info(f"Submission recieved from {request.remote_addr}: Name: {name}, Desc: {desc}, Addr: {addr}, Tags: {tags}, Cood: {lat}, {long}")

        submission = {
            "name": name,
            "desc": desc,
            "address": addr,
            "website": website,
            "location": {
                "type": "Point",
                "coordinates": [long,lat] #coordinates are in long, lat format
            },
            "tags": tags
        }

        submissions.insert_one(submission)

        return render_template("submit.html", title=title, submittedForm = True)

    else:
        return render_template("submit.html", title=title, submittedForm = False)
    
@app.route("/admin/newuser", methods=["GET","POST"])
def newAccount():
    if request.method == "POST":
        return {"username":request.form["username"],"password":generate_password_hash(request.form["password"])}
    return render_template("createAccount.html",title="Create New User")

def getUser(username:str):
    user = auth.find_one(
        {"username": username}
    )
    return user

def login():
    username = request.form["username"]
    password = request.form["password"]

    doc = getUser(username)
    try:
        success = check_password_hash(doc["password"], password)
    except TypeError:
        # if no users are found with a username, doc = None.
        success = False
    return success

@app.route("/admin", methods=["GET", "POST"])
def webLogin():
    error = None
    try:
        currentUsername = session["username"]
    except:
        currentUsername = None
    if currentUsername:
        return redirect("/admin/submissions", 302)
    if request.method == "POST":
        attempt = login()
        if attempt:
            session["username"] = request.form["username"]
            return redirect("/admin/submissions", 302)
        else:
            error = "Username or Password Incorrect."
        app.logger.info(f"{'Successful' if attempt else 'Failed'} login attempt by {request.form['username']}")
    return render_template("login.html", title="Login", error=error)

        

@app.route("/admin/submissions", methods=["GET","POST"])
def webSubmissions():
    # if no username is saved, the session is not logged in
    try:
        username = session["username"]
    except KeyError:
        return redirect("/admin",302)
    
    if request.method == "POST":
        decision = request.json
        try:
            location = submissions.find_one({"_id": ObjectId(decision["locationId"])})
        except:
            app.logger.error(f"User {username} sent a POST with a non-existant ObjectId")
            abort(400)
        app.logger.info(f"{username} has {'approved' if decision['pass'] else 'deleted'} submission {decision['locationId']}, {location['name']}")
        if decision["pass"]:
            restaurants.insert_one({
                "name": location["name"],
                "desc": location["desc"],
                "address": location["address"],
                "website": location["website"],
                "location": {
                    "type": "Point",
                    "coordinates": [location["location"]["coordinates"][0],location["location"]["coordinates"][1]] #coordinates are in long, lat format
                },
                "tags": location["tags"]
            })
        submissions.delete_one({"_id": ObjectId(decision["locationId"])})




    data = getSubmissions()
    results = []
    for doc in data:
        results.append(doc)

    return render_template("submissions.html", locations = results, username=username, length=len(results))

@app.errorhandler(404)
def error404(error):

    return render_template("404.html",title="Page not found")