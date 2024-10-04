from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(100), nullable=True)
    stair_climbs = db.relationship('StairClimb', backref='user', lazy=True)

    def total_stairs(self):
        return sum(climb.stairs_climbed for climb in self.stair_climbs)

class StairClimb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stairs_climbed = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
