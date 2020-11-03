#Dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#for MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

#Main webpage
@app.route("/")
def index():

    #Grabbing data from db
    mars = mongo.db.mars.find_one()

    #Applying db data to html template
    return render_template("index.html", mars=mars)

# Scrape, then Mongo DB
@app.route('/scrape')
def get():

    #database
    mars = mongo.db.mars

    #Script scrape part
    marsdata = scrape_mars.scrape()

    #Data stuff for database
    mars.update({}, marsdata, upsert=True)

    #Home
    return redirect("/", code=302)


#Main
if __name__ == "__main__":
    app.run()
