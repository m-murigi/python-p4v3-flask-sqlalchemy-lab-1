# # server/app.py
# #!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

# Add view here
@app.route("/earthquakes/<int:id>", methods=["GET"])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if not earthquake :
        return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)
    return make_response(jsonify(earthquake.to_dict()), 200)


@app.route('/earthquakes/magnitude/<float:magnitude>',methods =['GET'])

def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_list = [quake.to_dict() for quake in quakes]
    response = {"count": len(quakes_list), "quakes": quakes_list}
    return make_response(jsonify(response), 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
