# Flask Restaurant Review System

This Flask application is a web application for managing restaurants and reviews. 

**Features:**

* **User Management:**
    * User Registration
    * User Login 
    * User Logout

* **Restaurant Management (Admin):**
    * View all restaurants
    * Add new restaurants
    * Edit existing restaurants
    * Delete restaurants

* **Review Management:**
    * View restaurant reviews
    * Add reviews for restaurants
    * Edit reviews (by the user who wrote them)
    * Delete reviews (by the user who wrote them)

**Technologies:**

* **Python:** The primary programming language.
* **Flask:** The web framework used to build the application.
* **Flask-MySQL:** For interacting with the MySQL database.
* **bcrypt:** For password hashing and security.
* **HTML, CSS, JavaScript:** For frontend presentation.

**Installation:**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/mdzubayerhossain/Restaurant_Review_System.git

2. **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv 
    source venv/bin/activate  # On Linux/macOS
    .\venv\Scripts\activate  # On Windows
  Configure Database:

**3. Create a MySQL database.**
Update app.config in app.py with your database credentials:
  ```bash
    app.config['MYSQL_HOST'] = 'your_host' 
    app.config['MYSQL_USER'] = 'your_user' 
    app.config['MYSQL_PASSWORD'] = 'your_password' 
    app.config['MYSQL_DB'] = 'your_database_name'



**Run the Application:**
  python app.py 
