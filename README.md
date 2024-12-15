Project Overview

The Quantum Dice Roller is a Flask-based web application designed to simulate dice rolls and dynamically track user statistics. 
This project integrates Python programming, Flask web framework, and SQLite database management to provide an engaging platform for 
exploring randomness and probability. It offers a user-friendly interface for registration, secure login, and interaction with 
dice roll functionalities, while also calculating and displaying detailed statistics for each user.


Features:

1. User Authentication
Users can register and log in securely.
Passwords are stored securely using the database.

2. Dice Rolling Mechanism
Simulates dice rolls using Python’s os.urandom() for entropy.
Each roll result is recorded in the database with a timestamp.

3. Statistics Tracking
Tracks and calculates:
Total rolls
Highest roll
Lowest roll
Average roll
Updates statistics dynamically after each roll.

4. Roll History
Displays the user's roll history, including the result and timestamp of each roll.
Allows users to delete specific rolls.

5. Database Management
SQLite is used for data persistence with tables for users, dice rolls, and statistics.
Efficient queries ensure data integrity and fast retrieval.


FILE STRUCTURE
quantum-dice-roller/
├── app.py               # Main Flask application
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── roll.html        # Dice rolling page
│   ├── history.html     # Roll history page
│   ├── statistics.html  # Statistics page
├── static/              # Static files (CSS, JS, images)
│   └── styles.css       # Custom CSS
├── quantum_dice_roller.db # SQLite database file (created at runtime)
├── README.md            # Documentation
├── requirements.txt     # Project dependencies



Core Python Concepts

1. Encapsulation
Functions like get_db_connection() and roll_die() encapsulate key operations, ensuring reusability and maintainability.

2. Database Management
SQLite handles persistent data storage for user credentials, roll results, and statistics.

3. Session Management
Flask's session functionality ensures personalized and secure user interactions.

4. Randomness Simulation
Dice rolls use system-level entropy via:
roll_die(min_val=1, max_val=6):
    return (int.from_bytes(os.urandom(1), 'big') % (max_val - min_val + 1)) + min_val


Sustainable Development Goals (SDGs)

1. SDG 4: Quality Education
Provides an interactive platform for learning about randomness and programming concepts.

2. SDG 9: Industry, Innovation, and Infrastructure
Demonstrates the integration of modern tools like Flask and SQLite for innovative web application design.****
