from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify
from sklearn.externals import joblib
from flask_sqlalchemy import SQLAlchemy
from models import Result
from db import db, app


#app = Flask(__name__)

#export APP_SETTINGS="config.DevelopmentConfig
#app.config.from_object(os.environ["APP_SETTINGS"])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

@app.route("/")
def index():
    response = make_response(render_template("index.html"))
    return response

@app.route("/predict", methods=['POST'])
def predict():
    if request.method=='POST':
        regressor = joblib.load("./linear_regression_model.pkl")
        data = dict(request.form.items())
        years_of_experience = float(data["YearsExperience"])
        prediction = regressor.predict([[years_of_experience]])

        try:
            response = make_response(render_template(
            "predicted.html",
            prediction = float(prediction)
            ))
        except ValueError as e:
            print(e)

            return jsonify("Please enter a number.")

        result = Result(
            YearsExperience=float(years_of_experience),
            Prediction=float(prediction)
        )
        db.session.add(result)
        db.session.commit()
        print(db)

        return response

if __name__ == '__main__':
    app.run(debug=True)