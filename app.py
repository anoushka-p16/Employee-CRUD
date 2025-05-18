# Main Flask web application
from flask import Flask, render_template, request, redirect, abort
from models import db, EmployeeModel

app = Flask(__name__) # Initialize Flask app

# Link SQLite DB with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) # Initialize SQLAlchemy

# CRUD Operations

# Create
@app.route('/data/create', methods = ['GET', 'POST'])
def create(): # Runs when someone goes to /data/create
    if request.method == 'POST':
        eid = request.form['employee_id']

        # Checks if this id already exists
        if EmployeeModel.query.filter_by(employee_id=eid).first():
            return f"Employee with ID {eid} already exists."
        
        # Create a new employee
        e = EmployeeModel(
            employee_id=request.form['employee_id'],
            name=request.form['name'],
            age=request.form['age'],
            position=request.form['position']
        )
        db.session.add(e) # Queues the new employee to be added
        db.session.commit() # Commit the changes to the database
        return redirect('/data')
    # Shows the blank form
    return render_template('createpage.html')

# Retrieve all employees
@app.route('/data')
def list_employees():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html', employees=employees)

# Retrieve a single employee by id
@app.route('/data/<int:id>')
def show_employee(id):
    emp = EmployeeModel.query.filter_by(employee_id=id).first()
    if not emp:
        abort(404, f"Employee {id} not found")
    return render_template('data.html', employee=emp)

# Update
@app.route('/data/<int:id>/update', methods=['GET','POST'])
def update(id):
    emp = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if not emp:
            abort(404)
        # Delete the old employee record
        db.session.delete(emp)
        db.session.commit()
        # Create an updated record
        updated = EmployeeModel(
            employee_id=id,
            name=request.form['name'],
            age=request.form['age'],
            position=request.form['position']
        )
        db.session.add(updated)
        db.session.commit()
        return redirect(f'/data/{id}')
    return render_template('update.html', employee=emp)

# Delete
@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    emp = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if not emp:
            abort(404)
        db.session.delete(emp)
        db.session.commit()
        return redirect('/data')
    return render_template('delete.html')

# Run
if __name__ == '__main__':
    # Create tables if they don't exist yet
    with app.app_context():
        db.create_all()

    # App run details
    app.run(host='localhost', port=5000, debug=True)
