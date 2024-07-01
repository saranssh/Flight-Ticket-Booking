# Flight Ticket Booking Application

This is a Flask-based web application for booking flights, managing bookings, and administering flights.

## Features

- **User Authentication**: Users can sign up, log in, and log out. Passwords are hashed using bcrypt for security.
- **User Roles**: Admin users have additional privileges to manage flights and view all bookings.
- **Flight Management**: Admins can add new flights with details like flight name, number, date, and total seats.
- **Booking System**: Users can search for flights, book available tickets, and view their own bookings.

## Directory Structure

-instance/
-db.sqlite
-static/
  └── css/
  └── style.css
-templates/
  ├── add_flight.html
  ├── admin_dashboard.html
  ├── base.html
  ├── book_tickets.html
  ├── index.html
  ├── login.html
  ├── search_flight.html
  ├── signup.html
  ├── user_dashboard.html
  └── view_bookings.html
-app.py
