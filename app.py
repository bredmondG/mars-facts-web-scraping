from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import mars_scrape


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scrapedb")


@app.route("/")
def home():

    mars_data = mongo.db.collection.find_one()

    return render_template("news.html", mars=mars_data)

@app.route("/scrape")
def scrape():

    mars = mars_scrape.scrape()
    mongo.db.collection.update({}, mars, upsert=True)
    return redirect("/")
    
    

if __name__ == "__main__":
    app.run(debug=True)