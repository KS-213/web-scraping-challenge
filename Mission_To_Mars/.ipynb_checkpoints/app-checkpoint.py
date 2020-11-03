#Dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Flask app
app = Flask(__name__)

#Setting up MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

#Main page
@app.route("/")
def index():

    #Grabbing data from db
    mars = mongo.db.mars.find_one()

    #Applying db data to html template
    return render_template("index.html", mars=mars)

# Scrape Data and pull into Mongo DB
@app.route('/scrape')
def get():

    #Creating db
    mars = mongo.db.mars

    #Running scraping script to get data
    marsdata = scrape_mars.scrape()

    #Adding these data to the db
    mars.update({}, marsdata, upsert=True)

    #Returning to Home Page
    return redirect("/", code=302)


#Main
if __name__ == "__main__":
    app.run()
