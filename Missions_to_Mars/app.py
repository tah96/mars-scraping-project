from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create Flask application and connect to MongoDB URL for connection

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", listings=mars_data)


@app.route("/scrape")
def scraper():
    listings = mongo.db.mars_data
    listings_data = scrape_mars.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)