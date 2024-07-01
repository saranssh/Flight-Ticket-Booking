# Flight Ticket Booking Application

- This is a Flask-based web application for booking flights, managing bookings, and administering flights.

- The application is hosted on [PythonAnywhere](https://apexrider.pythonanywhere.com/).

## Features

- **User Authentication**: Users can sign up, log in, and log out. Passwords are hashed using bcrypt for security.
- **User Roles**: Admin users have additional privileges to manage flights and view all bookings.
- **Flight Management**: Admins can add new flights with details like flight name, number, date, and total seats.
- **Booking System**: Users can search for flights, book available tickets, and view their own bookings.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
2. **Run the application:**

   ```bash
   python app.py
   ```
     The application will be accessible at http://localhost:5000.

3. **Database initialization:**

   -The SQLite database file db.sqlite is used to store data.
   -Tables are created automatically on application startup.

4. **Usage:**

   -Navigate to http://localhost:5000 to access the application.

5. **Credits:**

    This application was developed by Saransh S.
