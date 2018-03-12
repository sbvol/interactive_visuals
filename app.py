# import necessary libraries
import numpy as np
from flask import (
    Flask,
    render_template,
    jsonify,
    request)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Database Setup
#################################################

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from sqlalchemy import create_engine, MetaData, inspect

engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Create our session (link) from Python to the DB
session = Session(engine)

Sam_Meta = Base.classes.samples_metadata
OTU = Base.classes.otu

@app.before_first_request
def setup():
    db.create_all()


#################################################
# Routes
#################################################

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/names')
def bb_names():
    bb_names = []
    results = session.query(Sam_Meta.SAMPLEID).all()
    
    for r in results:
        bb_names.append("BB_" + str(r[0]))

    return bb_names

@app.route('/otu')
def otu_desc():
    otu_desc = []
    results = session.query(OTU.lowest_taxonomic_unit_found).all()

    for r in results:
        otu_desc.append(str(r[0]))

    return otu_desc


@app.route('/metadata/<sample>')
def metadata(sample):
    sampleId = sample.split('_')
    
    results = session.query(Sam_Meta).filter(Sam_Meta.SAMPLEID == sampleId[1]).first()

    sam_meta = {}
    sam_meta = {
    'Age':results.AGE,
    'BBType':results.BBTYPE,
    'Ethnicity':results.ETHNICITY,
    'Gender':results.GENDER,
    'Location':results.LOCATION,
    'SampleID':results.SAMPLEID
    }

    return sam_meta

@app.route('/wfreq/<sample>')
def wfreq():
    sampleId = sample.split('_')
    
    results = session.query(Sam_Meta).filter(Sam_Meta.SAMPLEID == sampleId[1]).first()

    return results.WFREQ    


@app.route('/samples/<sample>')
    sampleId = sample
    
    Sam = Base.classes.samples
    from sqlalchemy import desc
    results = session.query(Sam.otu_id, Sam.sampleId).order_by(desc(Sam.sampleId))

    sam_dict = {}
    sam_otu_id_list = []
    sam_val_list = []
    for i in range(3674):
        sam_otu_id_list.append(results[i][0])
        sam_val_list.append(results[i][1])
        sam_dict['otu_id'] = sam_otu_id_list
        sam_dict['sample_value'] = sam_val_list

    return sam_dict

#@app.route("/send", methods=["GET", "POST"])
#def send():
#    if request.method == "POST":
#        nickname = request.form["nickname"]
#       age = request.form["age"]

#        pet = Pet(nickname=nickname, age=age)
#        db.session.add(pet)
#        db.session.commit()

#        return "Thanks for the form data!"

#    return render_template("form.html")


#@app.route("/pets")
#def list_pets():
#    results = db.session.query(Pet.nickname, Pet.age).all()

#    pets = []
#    for result in results:
#        pets.append({
#            "nickname": result[0],
#            "age": result[1]
#        })
#    return jsonify(pets)



if __name__ == "__main__":
    app.run()
