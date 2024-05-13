#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, WaterThing, UnderSeaHouse # ADD OTHER MODELS HERE


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)


# ROUTES


@app.get('/')
def index():
    return { "stuff": "I am stuff" }, 404

@app.get('/water-things')
def get_all_water_things():
    return[wt.to_dict() for wt in WaterThing.query.all()], 200

@app.get('/underseahouse')
def get_underseahouse():
    return[uh.to_dict() for uh in UnderSeaHouse.query.all()], 200

@app.get('/water-things/<int:id>')
def get_one_water_thing(id):
    water_thing = WaterThing.query.where(WaterThing.id ==id).first()
    if water_thing:
        return water_thing.to_dict(), 200
    else:
        return {"error": "Not Found"}, 404
    

@app.get('/underseahouse/<int:id>')
def get_one_underseahouse(id):
    underseahouse = UnderSeaHouse.query.where(UnderSeaHouse.id ==id).first()
    if underseahouse:
        return underseahouse.to_dict(), 200
    else:
        return {"error":"Not Found"}, 404


@app.post('/water-things')
def post_water_things():
    new_water_thing = WaterThing(
        name=request.json['name'], 
        species=request.json['species']
    )
    db.session.add(new_water_thing)
    db.session.commit()
    return new_water_thing.to_dict(), 201

@app.post('/underseahouse')
def post_underseahouse():
    new_underseahouse = UnderSeaHouse(
        name = request.json['name'],
        location = request.json['location']
    )
    db.session.add(new_underseahouse)
    db.session.commit()
    return new_underseahouse.to_dict(), 201


@app.patch('/water-things/<int:id>')
def patch_water_thing(id):
    water_thing_to_update = WaterThing.query.where(WaterThing.id==id).first()
    if water_thing_to_update:
        # name = request.json['name']
        for key in request.json.keys(): #'name'/'species'
            #set all keys for each key in request.json
            setattr(water_thing_to_update, key, request.json[key])
        db.session.add(water_thing_to_update)
        db.session.commit()
        return water_thing_to_update.to_dict(), 202
    else:
        return {"error":"Not Found"}, 404
    

@app.patch('/underseahouse/<int:id>')
def underseahouse(id):
    underseahouse_to_update = UnderSeaHouse.query.where(UnderSeaHouse.id == id).first()
    if underseahouse_to_update:
        for key in request.json.keys():
            setattr(underseahouse_to_update, key, request.json[key])
        db.session.add(underseahouse_to_update)
        db.session.commit()
        return underseahouse_to_update.to_dict(),202
    else:
        return {"error":"Not Found"}, 404
    



@app.delete('/water-things/<int:id>')
def delete_water_things(id:int):
    water_thing_to_delete = WaterThing.query.where(WaterThing.id ==id).first()
    if water_thing_to_delete:
        db.session.delete(water_thing_to_delete)
        db.session.commit()
        return {}, 202
        # return [wt for wt in WaterThing.query.all()], 202
    else:
        return {"error":"Not Found"}, 404


@app.delete('/underseahouse/<int:id>')
def delete_underseahouse(id:int):
    underseahouse_to_delete = UnderSeaHouse.query.where(UnderSeaHouse.id ==id).first()
    if underseahouse_to_delete:
        db.session.delete(underseahouse_to_delete)
        db.session.commit()
        return{}, 202
    else:
        return{"error":"Not Found"}, 404




# APP RUN

if __name__ == '__main__':
    app.run(port=5555, debug=True)
