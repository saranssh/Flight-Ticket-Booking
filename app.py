from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'supersecretkey'

#Connecting to my sql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#required database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_name = db.Column(db.String(120), nullable=False)
    flight_number = db.Column(db.String(60), nullable=False)
    date = db.Column(db.String(60), nullable=False)
    total_seats = db.Column(db.Integer, default=60)
    available_seats = db.Column(db.Integer, default=60)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    flight = db.relationship('Flight', backref=db.backref('bookings', lazy=True))


#defining the table as per reuirements
def create_tables():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@example.com').first():
            hashed_password = bcrypt.hashpw('adminpassword'.encode('utf-8'), bcrypt.gensalt())
            admin_user = User(email='admin@example.com', password=hashed_password.decode('utf-8'), is_admin=True)
            db.session.add(admin_user)
            db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.checkpw(data['password'].encode('utf-8'),
            user.password.encode('utf-8')):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('user_dashboard' if not user.is_admin else 'admin_dashboard'))
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User(email=data['email'], password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/user_dashboard')
def user_dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('user_dashboard.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('user_id') or not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/search_flight', methods=['GET', 'POST'])
def search_flight():
    if request.method == 'POST':
        data = request.form
        flights = Flight.query.filter(
            Flight.flight_name.like(f"%{data['flight_name']}%"),
            Flight.date == data['date'],
            Flight.flight_number == data['flight_number']
        ).all()
        return render_template('search_flight.html', flights=flights)
    return render_template('search_flight.html')

@app.route('/book_tickets', methods=['GET', 'POST'])
def book_tickets():
    if request.method == 'POST':
        if not session.get('user_id'):
            return redirect(url_for('login'))
        
        data = request.form
        flight_id = data.get('flight_id')
        flight = Flight.query.get(flight_id)
        
        if not flight_id or not flight:
            error = 'Flight ID is required and must be valid.'
            return render_template('book_tickets.html', error=error)

        if flight.available_seats > 0:
            flight.available_seats -= 1
            booking = Booking(user_id=session['user_id'], flight_id=flight_id)
            db.session.add(booking)
            db.session.commit()
            return render_template('book_tickets.html', message='Booking successful!')
        else:
            error = 'No available seats for this flight.'
            return render_template('book_tickets.html', error=error)
    
    flights = Flight.query.all()
    return render_template('book_tickets.html', flights=flights)



@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if not session.get('user_id') or not session.get('is_admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.form
        new_flight = Flight(
            flight_name=data['flight_name'],
            flight_number=data['flight_number'],
            date=data['date'],
            total_seats=data['total_seats'],
            available_seats=data['total_seats']
        )
        db.session.add(new_flight)
        db.session.commit()
        return render_template('add_flight.html', message='Flight added successfully!')
    return render_template('add_flight.html')

@app.route('/view_bookings', methods=['GET'])
def view_bookings():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    if session.get('is_admin'):
        bookings = Booking.query.all()
    else:
        bookings = Booking.query.filter_by(user_id=session['user_id']).all()
        
    return render_template('view_bookings.html', bookings=bookings)



if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
