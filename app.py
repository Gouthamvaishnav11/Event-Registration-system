from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventdetails.db'

# Creating an object of the SQLAlchemy class
database = SQLAlchemy(app)

# Python class to insert data into the table
class Details(database.Model):
    sno = database.Column(database.Integer, primary_key=True)
    event_name = database.Column(database.String(100), nullable=False)
    date = database.Column(database.String(20), nullable=False)
    name = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False)
    phone = database.Column(database.String(20), nullable=False)


# Route for index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        event = request.form.get('event_name')
        date = request.form.get('date')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Add it to the database
        member = Details(event_name=event, date=date, name=name, email=email, phone=phone)
        database.session.add(member)
        database.session.commit()

        # Return the index.html
        return redirect('/')

    else:
        # Fetching all tasks from details database
        alldetails = Details.query.all()
        return render_template('index.html', alldetails=alldetails)

# Route to delete an event
@app.route('/delete')
def delete():
    # Extracting the sno
    serial_number = request.args.get('sno')

    # Fetching details with sno=serial_number
    member = Details.query.filter_by(sno=serial_number).first()

    # Deleting the details
    database.session.delete(member)
    database.session.commit()

    # Reassign serial numbers
    alldetails = Details.query.order_by(Details.sno).all()
    for index, member in enumerate(alldetails, start=1):
        member.sno = index
    database.session.commit()

    # Redirect to index.html
    return redirect('/')

# Route to update event details
@app.route('/update', methods=['GET', 'POST'])
def update():
    # Getting the sno for update
    serial_number = request.args.get('sno')

    # Fetching the details from database to update
    reqdetails = Details.query.filter_by(sno=serial_number).first()

    if request.method == "POST":
        # Fetching the updated values
        updatedevent = request.form.get('event_name')
        updateddate = request.form.get('date')
        updatedname = request.form.get('name')
        updatedemail = request.form.get('email')
        updatedphone = request.form.get('phone')

        # Changing the values of the existing details
        reqdetails.event_name = updatedevent
        reqdetails.date = updateddate
        reqdetails.name = updatedname
        reqdetails.email = updatedemail
        reqdetails.phone = updatedphone

        # Committing the changes
        database.session.commit()

        # Redirect to index.html
        return redirect('/')

    else:
        # Rendering the update.html page
        return render_template('update.html', reqdetails=reqdetails)

if __name__ == '__main__':
    app.run(debug=True, port=2000)
