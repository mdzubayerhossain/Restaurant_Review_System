
**Flask Restaurant Review Application**

This Flask application is a restaurant review system that allows users to sign up, log in, view restaurants, and write reviews. It also allows admins to manage restaurants and reviews.

**Features:**

* User Signup and Login
* Admin Signup and Login
* View Restaurants (for both users and admins)
* Insert Reviews (for users)
* Delete Reviews (by users who wrote them)
* Update Reviews (by users who wrote them)
* View Reviews (for admins and users who wrote them)
* Insert Restaurants (for admins)
* Delete Restaurants (by admins who created them)
* Update Restaurants (by admins who created them)

**Dependencies:**

* Flask
* Flask-MySQL
* bcrypt

**Installation:**

1. Clone this repository.
2. Create a virtual environment and activate it.
3. Install the required dependencies:



4. Create a MySQL database and configure the connection details in the `app.config` dictionary in the Flask application file (`app.py`).

**Running the application:**

1. Start the Flask development server:

```bash
python app.py
