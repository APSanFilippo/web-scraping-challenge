from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    All_data= mongo.db.All_data.find_one()
    return render_template("index.html", All_data=All_data)


@app.route("/scrape")
def scraper():
    All_data = mongo.db.All_data
    All_data = scrape_mars.scrape()
    All_data.update({}, All_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)