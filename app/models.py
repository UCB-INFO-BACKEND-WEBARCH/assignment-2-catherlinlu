from app import db
from datetime import datetime

class Category (db.Model): 
    __tablename__ = "Category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique = True)
    color = db.Column(db.String(7), nullable=True)
    tasks = db.relationship('Tasks', backref='Category', lazy=True)

class Tasks (db.Model):
     __tablename__ = "Tasks"
     id = db.Column(db.Integer, primary_key = True)
     title = db.Column(db.String(100), nullable = False)
     description = db.Column(db.String(500), nullable = True)
     completed = db.Column(db.Boolean, default = False)
     due_date = db.Column(db.DateTime, nullable = True)
     category_id = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable = True)
     created_at = db.Column(db.DateTime, default=datetime.utcnow)
     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate = datetime.utcnow)

#requirement: a Category has many Tasks. A Task belongs to one Category (optional)

    
