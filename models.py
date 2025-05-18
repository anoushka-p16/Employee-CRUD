# Model - Python Class representing a table in the database
# Contains information regarding the table structure

# models.py is a file that saves all the DB information and models

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EmployeeModel(db.Model):
    __tablename__ = "Employee Table"

    id = db.Column(db.Integer, primary_key=True) # Automatically increments key
    employee_id = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))

    def __init__(self, employee_id, name, age, position):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.position = position

    # How the object is represented when printed
    def __repr__(self):
        return f"{self.name}:{self.employee_id}"
    