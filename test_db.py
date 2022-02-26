from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://Taffer:3kpSf42b@Taffer.mysql.pythonanywhere-services.com/Taffer$competitors"

db = SQLAlchemy(app)

class vandn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    published_at = db.Column(db.String(100))
    title = db.Column(db.String(150))
    view_count = db.Column(db.Integer)

    def __init__(self, date_time, published_at, title, view_count):
        self.date_time = date_time
        self.published_at = published_at
        self.title = title
        self.view_count = view_count

    def __repr__(self):
        return 'Published at %s; Title: %s View count: %i' % (self.published_at, self.title, self.view_count)

db.create_all()
db.session.commit()