from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Taffer:189gk642@Taffer.mysql.pythonanywhere-services.com/Taffer$test_youtubue'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	json_data = db.Column(db.JSON, nullable=False)

	def __init__(self, id, json_data):
		self.id = id
		self.json_data = json_data

	def __repr__(self):
		return 'json_data %s' % self.json_data