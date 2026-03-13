from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- DATABASE CONFIG ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flight_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_city = db.Column(db.String(50), nullable=False)
    to_city = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    flight = db.relationship('Flight', backref=db.backref('bookings', lazy=True))
    passenger_names = db.Column(db.String(500), nullable=False)  # comma-separated
    travel_date = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    date_booked = db.Column(db.String(50), default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# --- FLIGHT SYSTEM SETUP ---
def add_sample_flights():
    if Flight.query.first():
        return  # flights already exist

    cities = [
        "Chennai", "Delhi", "Mumbai", "Bangalore",
        "Hyderabad", "Kolkata", "Goa", "Ahmedabad", "Pune", "Jaipur"
    ]
    flight_id = 1
    for from_city in cities:
        for to_city in cities:
            if from_city != to_city:
                price = 3000 + (flight_id * 100)
                seats = 20
                flight = Flight(from_city=from_city, to_city=to_city, price=price, seats_available=seats)
                db.session.add(flight)
                flight_id += 1
    db.session.commit()

# --- ROUTES ---

@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    flights = Flight.query.all()
    cities = sorted(list(set([f.from_city for f in flights] + [f.to_city for f in flights])))
    return render_template("index.html", flights=flights, cities=cities, username=session["username"])

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect(url_for("signup"))

        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["username"] = username
            flash("Login successful!")
            return redirect(url_for("home"))

        flash("Invalid username or password!")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully!")
    return redirect(url_for("login"))

@app.route("/book/<int:flight_id>", methods=["GET", "POST"])
def book_flight(flight_id):
    if "username" not in session:
        return redirect(url_for("login"))

    flight = Flight.query.get_or_404(flight_id)
    if request.method == "POST":
        passenger_names = request.form.getlist("passenger_name")
        travel_date = request.form["travel_date"]

        if len(passenger_names) > flight.seats_available:
            flash("Not enough seats available!")
            return redirect(url_for("book_flight", flight_id=flight_id))

        # Reduce available seats
        flight.seats_available -= len(passenger_names)
        booking = Booking(
            flight_id=flight.id,
            passenger_names=",".join(passenger_names),
            travel_date=travel_date,
            username=session["username"]
        )
        db.session.add(booking)
        db.session.commit()

        total_price = len(passenger_names) * flight.price
        return render_template("payment.html", booking=booking, passengers=len(passenger_names), total_price=total_price)

    today = datetime.date.today().strftime("%Y-%m-%d")
    return render_template("book.html", flight=flight, today=today, username=session["username"])

@app.route("/bookings")
def bookings():
    if "username" not in session:
        return redirect(url_for("login"))

    user_bookings = Booking.query.filter_by(username=session["username"]).all()
    return render_template("bookings.html", bookings=user_bookings, username=session["username"])

@app.route("/about")
def about():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("about.html", username=session["username"])

@app.route("/contact")
def contact():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("contact.html", username=session["username"])

# --- MAIN ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()       # Create tables inside app context
        add_sample_flights()  # Add sample flights
    app.run(debug=True)